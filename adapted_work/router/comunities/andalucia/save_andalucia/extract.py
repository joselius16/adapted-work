import re
import time
from typing import List

import requests
from bs4 import BeautifulSoup
from loguru import logger
from sqlmodel import Session, select
from tqdm import tqdm

from adapted_work.database.connection import engine
from adapted_work.database.tables import Comunity
from adapted_work.settings import comunities_codes, settings

# base_url = "https://www.juntadeandalucia.es/organismos/iaap/areas/empleo-publico/procesos-selectivos/detalle/"
# start_id = 514556
# end_id = 514560


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


def get_page_info(urls: List[str]) -> List[Comunity]:
    """Get page information and return it into andalucia schema table.

    Args:
        urls (List[str]): List of urls availables

    Returns:
        List[Comunity]: list with vacancies
    """
    data_andalucia = []

    for url in urls:
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            # Analyze html
            soup = BeautifulSoup(response.text, "html.parser")

            # TODO: segun la estructura de andalucia hay que hacer esto
            # element = soup.find(
            #     class_="block block-layout-builder block-field-blocknodeprocesos-selectivosnumb-plazas-totales-division"
            # )
            element = soup.find(class_="encab-secc col-12")

            if element:
                # 1. Disability
                disability_text = None
                match = re.search(
                    r"(\d+)\s?\(Cupo de discapacidad general\)", element.text.strip()
                )
                if match:
                    disability_text = match.group(1)
                    # break

                # if disability exists
                if disability_text:
                    # Find more data
                    element_str = element.prettify()
                    # 2. Specialty
                    # specialty_match =
                    pattern = r'<div class="views-label views-label-field-taxo-personal-3 field__label">\s*Especialidad\s*</div>\s*<div class="field-content field__item">\s*(.*?)\s*</div>'
                    specialty_match = re.search(pattern, element_str, re.DOTALL)
                    specialty = specialty_match.group(1).strip()

                    # 3. Qualification
                    pattern = r'<div class="views-label views-label-field-taxo-personal-2 field__label">\s*Cuerpo/Grupo\s*</div>\s*<div class="field-content field__item">\s*(.*?)\s*</div>'
                    qualification_match = re.search(pattern, element_str, re.DOTALL)
                    qualification = qualification_match.group(1).strip()

                    # 4. Type personal
                    pattern = r'<div class="views-label views-label-field-taxo-personal-1 field__label">\s*Tipo de personal\s*</div>\s*<div class="field-content field__item">\s*(.*?)\s*</div>'
                    type_personnel_match = re.search(pattern, element_str, re.DOTALL)
                    type_personnel = type_personnel_match.group(1).strip()

                    # 5. Date
                    pattern = r'<div class="views-label views-label-field-taxo-estado-1 field__label">\s*Estado\s*</div>\s*<div class="field-content field__item">\s*(.*?)\s*</div>'
                    state_match = re.search(pattern, element_str, re.DOTALL)
                    state = state_match.group(1).strip()

                    disability_number = int(disability_text)
                    data_andalucia.append(
                        Comunity(
                            id_comunity_type=comunities_codes.andalucia,
                            ext_url=url,
                            disability_vacancies=disability_number,
                            specialty=specialty,
                            qualifycation=qualification,
                            type_of_personnel=type_personnel,
                            dates=state,
                        )
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
                statement = select(Comunity).where(Comunity.ext_url == data.ext_url)
                result = session.exec(statement).first()

                if result:
                    logger.info(f"Url {data.ext_url} already in database.")
                    continue

                session.add(data)
                logger.info(f"saving: {data.ext_url}")

            session.commit()

        logger.info("Executed succesfully.")

    except Exception as e:
        logger.error("Cannot save into database.")


if __name__ == "__main__":
    save_andalucia(
        settings.base_url_andalucia,
        settings.start_id_andalucia,
        settings.end_id_andalucia,
    )
