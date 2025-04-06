import re
import time
from typing import List

import requests
from bs4 import BeautifulSoup
from loguru import logger
from sqlmodel import Session, select
from tqdm import tqdm

from adapted_work.database.connection import engine
from adapted_work.database.tables import Comunity, Jobs
from adapted_work.settings import settings, database_settings
from adapted_work.utils.process_data import save_into_database

base_url = "https://www.juntadeandalucia.es/organismos/iaap/areas/empleo-publico/procesos-selectivos/detalle/"
start_id = 514556
end_id = 514560


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
        url = f"{base_url}{i}.html"

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


def get_page_info(urls: List[str]) -> List[Jobs]:
    """Get page information and return it into andalucia schema table.

    Args:
        urls (List[str]): List of urls availables

    Returns:
        List[Jobs]: list with vacancies
    """
    data_andalucia = []

    for url in urls:
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            # Analyze html
            soup = BeautifulSoup(response.text, "html.parser")
            text_items = soup.get_text()

            # TODO: segun la estructura de andalucia hay que hacer esto
            element = soup.find(
                class_="block block-layout-builder block-field-blocknodeprocesos-selectivosnumb-plazas-totales-division"
            )

            if element:
                field_items = element.find_all("div", class_="field__item")

                disability_text = None
                for item in field_items:
                    # regex
                    match = re.search(
                        r"(\d+)\s?\(Cupo de discapacidad general\)", item.text.strip()
                    )
                    if match:
                        disability_number = int(match.group(1))
                        if disability_number > 0:

                            logger.info(f"Disability number: {disability_number}")

                            # Initializing variables
                            title = None
                            type_personnel = None
                            dates = None
                            qualification = None
                            specialty = None

                            # Title
                            match = re.search(r"^[ \n]*([A-Z]\d\.\d{4}.*?Junta de Andalucía)[ \n]*$", text_items, re.MULTILINE)
                            if match:
                                title = match.group(1).strip()
                            
                            # Type of personnel
                            match = re.search(r"Tipo de personal\s*(.+?)\s*Cuerpo/?Grupo", text_items)
                            if match:
                                type_personnel = match.group(1).strip()

                            # 5. Qualification
                            match = re.search(r"Cuerpo/?Grupo\s*(.+?)\s*Especialidad", text_items)
                            if match:
                                qualification = match.group(1).strip()

                            # Dates
                            match = re.search(r"Estado\s*(.*?)(?:\n\s*\n\s*\n|\n\s*[A-Z][a-z]+)", text_items, re.DOTALL)
                            if match:
                                dates = match.group(1).strip()

                            # Specialty
                            match = re.search(r"Especialidad\s*([A-Z]\d\.\d{4}.*?)\s*(Año de Oferta Pública|Estado)", text_items, re.DOTALL)
                            if match:
                                specialty = match.group(1).strip()

                            data_andalucia.append(
                                Jobs(id_comunity=database_settings.comunity_id.andalucia,
                                    ext_url=url,
                                    disability_vacancies=disability_number,
                                    dates=dates,
                                    title=title,
                                    specialty=specialty,
                                    type_personnel=type_personnel,
                                    qualification=qualification
                                    )
                            )
                else:
                    logger.info("There aren't any disability vacancies.")
            else:
                logger.info("Couldn't get disability vacancies")
        else:
            logger.error(f"Coudn't get to url:{url} status: {response.status_code}")

    return data_andalucia


def save_andalucia(base_url: str, start_id: int, end_id: int) -> List[str]:
    """Save Andalucia data.

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
    data_andalucia = get_page_info(urls)

    save_into_database(data_andalucia)


if __name__ == "__main__":
    save_andalucia(
        settings.base_url_andalucia,
        settings.start_id_andalucia,
        settings.end_id_andalucia,
    )
