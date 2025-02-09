import re
import time
from typing import List

import requests
from bs4 import BeautifulSoup
from loguru import logger
from sqlmodel import Session, select
from tqdm import tqdm

from adapted_work.database.connection import engine
from adapted_work.database.tables import Andalucia
from adapted_work.settings import settings

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


def get_page_info(urls: List[str]) -> List[Andalucia]:
    """Get page information and return it into andalucia schema table.

    Args:
        urls (List[str]): List of urls availables

    Returns:
        List[Andalucia]: list with vacancies
    """
    data_andalucia = []

    for url in urls:
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            # Analyze html
            soup = BeautifulSoup(response.text, "html.parser")

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
                        disability_text = match.group(1)
                        break

                # if disability exists
                if disability_text:
                    disability_number = int(disability_text)
                    data_andalucia.append(
                        Andalucia(url=url, disability_vacancies=disability_number)
                    )
                    logger.info(f"Disability number: {disability_number}")
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

    try:
        logger.info("Saving into database.")
        with Session(engine) as session:
            for data in data_andalucia:
                statement = select(Andalucia).where(Andalucia.url == data.url)
                result = session.exec(statement).first()

                if result:
                    logger.info(f"Url {data.url} already in database.")
                    continue

                session.add(data)
                logger.info(f"saving: {data.url}")
            session.commit()

        logger.info("Executed succesfully.")

    except:
        logger.error("Cannot save into database.")


if __name__ == "__main__":
    save_andalucia(
        settings.base_url_andalucia,
        settings.start_id_andalucia,
        settings.end_id_andalucia,
    )
