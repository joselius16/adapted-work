import re
import time
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm

from adapted_work.database.tables import Comunity, Jobs
from adapted_work.settings import database_settings, settings
from adapted_work.utils.process_data import save_into_database

# Url de busqueda: http://juntaex.es/temas/trabajo-y-empleo/empleo-publico/buscador-de-empleo-publico?p_p_id=es_juntaex_paoc_presentacion_empleo_buscador_JuntaexEmpleoBuscadorPortlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_es_juntaex_paoc_presentacion_empleo_buscador_JuntaexEmpleoBuscadorPortlet_javax.portlet.action=%2Fcommand%2Faction%2FBuscadorEmpleoActionURL&p_auth=9XrfG3Jy
base_url = "https://www.juntaex.es/temas/trabajo-y-empleo/empleo-publico/buscador-de-empleo-publico/-/convocatoria/"
start_id = 1638
end_id = 1639


def get_endpoints(base_url: str, start_id: int, end_id: int) -> List[str]:
    """Get endpoints function.

    Args:
        base_url (str): Base url
        start_id (int): start id employ number
        end_id (int): end id

    Returns:
        List[str]: list with endpoints with employment
    """
    valid_urls = []

    for i in tqdm(range(start_id, end_id + 1)):
        url = f"{base_url}{i}"

        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                valid_urls.append(url)
                logger.info(f"Saved {url} in valid urls.")
        except requests.exceptions.Timeout:
            logger.debug(f"Timeout in {url}, skipping url.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in {url}: {e}")

        time.sleep(1)  # wait for next request

    return valid_urls


def get_page_info(urls: List[str]) -> List[Comunity]:
    """Get page information and return it into comunity schema table.

    Args:
        urls (List[str]): List of urls availables

    Returns:
        List[Comunity]: list with vacancies
    """
    data_extremadura = []

    for url in urls:
        try:
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text_items = soup.get_text()

                if text_items:
                    disability_number = 0  # Valor por defecto
                    match = re.search(r"Plazas turno discapacidad:\s*(\d+)", text_items)
                    if match:
                        disability_number = int(match.group(1))

                        logger.info(f"Disability number: {disability_number}")

                        # Initializing variables
                        title = None
                        type_personnel = None
                        dates = None
                        qualification = None
                        specialty = None

                        # Title
                        match = soup.find(class_="text-success")
                        if match:
                            title = match.get_text(strip=True)

                        # Type of personnel
                        match = re.search(
                            r"Cuerpo\s*/\s*Grupo:\s*(.+?)(?:\n|$)", text_items
                        )
                        if match:
                            type_personnel = match.group(1).strip()

                        # 5. Qualification
                        match = re.search(
                            r"Titulación requerida:\s*(.*?)\n", text_items
                        )
                        if match:
                            qualification = match.group(1).strip()

                        # Dates
                        match = re.search(
                            r"Fecha de finalización del plazo de solicitudes:\s*(.*?)\n",
                            text_items,
                        )
                        if match:
                            dates = match.group(1).strip()

                        # Specialty
                        match = re.search(
                            r"Especialidad / Categoría:\s*(.*?)\n", text_items
                        )
                        if match:
                            specialty = match.group(1).strip()

                        # Datetime now
                        date_now = datetime.now()
                        date_now = datetime(date_now.year, date_now.month, date_now.day)

                        data_extremadura.append(
                            Jobs(
                                id_comunity=database_settings.comunity_id.extremadura,
                                ext_url=url,
                                disability_vacancies=disability_number,
                                dates=dates,
                                saved_date=date_now,
                                title=title,
                                specialty=specialty,
                                type_personnel=type_personnel,
                                qualification=qualification,
                            )
                        )

                else:
                    logger.info("Couldn't get disability vacancies")
            else:
                logger.error(
                    f"Couldn't get to url: {url} status: {response.status_code}"
                )

        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")

    return data_extremadura


def save_extremadura(base_url: str, start_id: int, end_id: int) -> List[str]:
    """Save Extremadura data.

    Args:
        base_url (str): Base url
        start_id (int): start id employ number
        end_id (int): end id

    Returns:
        List[str]: list with endpoints with employment
    """
    logger.info("Getting endpoints.")
    urls = get_endpoints(base_url, start_id, end_id)

    logger.info("Getting page info.")
    data_extremadura = get_page_info(urls)

    save_into_database(data_extremadura)


if __name__ == "__main__":
    save_extremadura(
        "https://www.juntaex.es/temas/trabajo-y-empleo/empleo-publico/buscador-de-empleo-publico/-/convocatoria/",
        1625,
        1626,
    )
