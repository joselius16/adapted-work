import re
from typing import List

import requests
from bs4 import BeautifulSoup
from loguru import logger
from sqlmodel import Session, select

from adapted_work.database.connection import engine
from adapted_work.database.tables import Comunity, Jobs
from adapted_work.settings import settings, database_settings
from adapted_work.utils.process_data import save_into_database

url_api = "https://empleopublico.carm.es/web/pagina?IDCONTENIDO=62006&IDTIPO=100&RASTRO=c%24m61986%2C61991&BUSCAR_POR=CUERPO_OFERTA&CUERPOS_OFERTABLES=0&ESTADOS_OPOSICIONES=0&Buscar=Buscar"


def get_endpoints(base_url: str) -> List[str]:
    """Get endpoints function.

    Args:
        base_url (str): Base url
        start_id (int): start id employ number
        end_id (int): end id

    Returns:
        List[str]: list with endpoints with employment
    """
    valid_urls = []

    headers = {"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"}

    response = requests.get(base_url, headers=headers)

    if response.status_code != 200:
        logger.error("Error in status:", response.status_code)
        return

    data = response.text

    # regular expresion to get the content from webpage
    patron = r'<a href="(pagina\?IDCONTENIDO=[^"]+)"'

    # we are going to get the extensions from data
    urls = set(re.findall(patron, data))

    murcia_url = "https://empleopublico.carm.es/web/"
    valid_urls = [murcia_url + url.replace("&amp;", "&") for url in urls]
    logger.info("finished urls findings")

    return valid_urls


def get_page_info(urls: List[str]) -> List[Comunity]:
    """Get page information and return it into Comunity schema table.

    Args:
        urls (List[str]): List of urls availables

    Returns:
        List[Comunity]: list with vacancies
    """
    data_murcia = []

    for url in urls:
        try:
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                disability_number = 0
                match = re.search(r"Discapacidad: \s*(\d+)", soup.text.strip())
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
                        match = re.search(r'PROCESO SELECTIVO:\s*</th>\s*<td>\s*(.*?)\s*</td>', response.text, re.S)
                        if match:
                            title = match.group(1).strip()
                        
                        # Type of personnel
                        match = re.search(r'OPCIÓN, CUERPO, SUBGRUPO:\s*</th>\s*<td>\s*(.*?)\s*</td>', response.text, re.S)
                        if match:
                            type_personnel = match.group(1).strip()

                        # 5. Qualification
                        match = re.search(r'TITULACIÓN REQUERIDA:\s*</th>\s*<td>\s*(.*?)\s*</td>', response.text, re.S)
                        if match:
                            qualification = match.group(1).strip()

                        # Dates
                        match = re.search(r'PLAZO DE SOLICITUD ABIERTO:\s*</th>\s*<td>\s*(.*?)\s*</td>', response.text, re.S)
                        if match:
                            dates = match.group(1).strip()

                        # Specialty
                        match = re.search(r'OPCIÓN, CUERPO, SUBGRUPO:\s*</th>\s*<td>\s*(.*?)\s*</td>', response.text, re.S)
                        if match:
                            specialty = match.group(1).strip()

                        data_murcia.append(
                            Jobs(id_comunity=database_settings.comunity_id.murcia,
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
                    logger.info("Couldn't get disability vacancies")
            else:
                logger.error(
                    f"Couldn't get to url: {url} status: {response.status_code}"
                )

        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")

    return data_murcia


def save_murcia(base_url: str) -> List[str]:
    """Save Murcia data.

    Args:
        base_url (str): Base url
        start_id (int): start id employ number
        end_id (int): end id

    Returns:
        List[str]: list with endpoints with employment
    """
    logger.info("Getting endpoints.")
    urls = get_endpoints(base_url)

    logger.info("Getting page info.")
    data_murcia = get_page_info(urls)

    save_into_database(data_murcia)


if __name__ == "__main__":
    save_murcia(url_api)
