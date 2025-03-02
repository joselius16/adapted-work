import re
import time
from typing import List

import requests
from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm

from adapted_work.database.tables import Comunity
from adapted_work.settings import settings
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


def get_page_info(urls: List[str]) -> List[Comunity]:
    """Get page information and return it into andalucia schema table.

    Args:
        urls (List[str]): List of urls availables

    Returns:
        List[Andalucia]: list with vacancies
    """
    data_aragon = []

    for url in urls:
        try:
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                # Find the cell with the discapacity
                th = soup.find("th", string="Personas con discapacidad")
                if th:
                    td = th.find_next("td")
                    disability_number = 0
                    disability_number = (
                        int(td.get_text(strip=True))
                        if td
                        else logger.info("Couldn't get disability vacancies")
                    )

                    if disability_number > 0:
                        data_aragon.append(
                            Comunity(url=url, disability_vacancies=disability_number)
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
