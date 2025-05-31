import re
import time
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm

from adapted_work.database.tables import Jobs
from adapted_work.settings import database_settings
from adapted_work.utils.process_data import save_into_database


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


def get_page_info(urls: List[str]) -> List[Jobs]:
    """Get page information and return it into andalucia schema table.

    Args:
        urls (List[str]): List of urls availables

    Returns:
        List[Jobs]: list with vacancies
    """
    data_aragon = []

    for url in urls:
        try:
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text_items = soup.get_text()
                if text_items:
                    disability_number = 0
                    match = re.search(r"Personas con discapacidad\s*(\d+)", text_items)
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
                        match = re.search(r"Denominación:\s*(.+?)(?:\n|$)", text_items)
                        if match:
                            title = match.group(1).strip()

                        # Type of personnel
                        match = re.search(
                            r"Tipo de plaza y grupo:\s*(.+?)(?:\n|$)", text_items
                        )
                        if match:
                            type_personnel = match.group(1).strip()

                        # 5. Qualification
                        match = re.search(r"Titulación exigida:\s*(.*?)\n", text_items)
                        if match:
                            qualification = match.group(1).strip()

                        # Dates
                        match = re.search(
                            r"Periodo de presentación:\s*((?:.|\n)+?)(?:\n\w|\Z)",
                            text_items,
                        )
                        if match:
                            dates = match.group(1).strip()
                            dates = " ".join(dates.split())

                        # Specialty # TODO: Hay que ver que es mejor si clasificar por categoria o especialidad
                        match = re.search(r"Especialidad/Rama:\s*(.*?)\n", text_items)
                        if match:
                            specialty = match.group(1).strip()

                            # Datetime now
                            date_now = datetime.now()
                            date_now = datetime(
                                date_now.year, date_now.month, date_now.day
                            )

                        data_aragon.append(
                            Jobs(
                                id_community=database_settings.community_id.aragon,
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
                        logger.info(f"Disability number: {disability_number}")
                else:
                    logger.info("Couldn't get disability vacancies")
            else:
                logger.error(
                    f"Couldn't get to url: {url} status: {response.status_code}"
                )

        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")

    return data_aragon


def save_aragon(base_url: str, start_id: int, end_id: int) -> List[str]:
    """Save Aragon data.

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
    data_aragon = get_page_info(urls)

    save_into_database(data_aragon)


if __name__ == "__main__":
    save_aragon(
        "https://aplicaciones.aragon.es/oepc/oepc?dga_accion_app=mostrar_convocatoria&convocatoria_codigo=",
        240118,
        240119,
    )
