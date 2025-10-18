import json

from adapted_work.router.comunities.andalucia.save_andalucia.extract import \
    save_andalucia
from adapted_work.router.comunities.aragon.save_aragon.extract import \
    save_aragon
from adapted_work.router.comunities.extremadura.save_extremadura.extract import \
    save_extremadura
from adapted_work.router.comunities.murcia.save_murcia.extract import \
    save_murcia
# TODO: Hay que ver como importamos aqui el settings
from adapted_work.scheduler.schema_model import (comunity_base_url,
                                                 comunity_names, range_id,
                                                 web_pages_ids)


def read_webpages_ranges() -> dict:
    """Read id range document.

    Args:
        web_pages_id (dict): _description_

    Returns:
        dict: _description_
    """
    with open(web_pages_ids, "r") as file:
         web_pages_range = json.load(file)
    return web_pages_range


def save_data(web_pages_id: dict) -> dict:
    """Save data from webpages.

    Args:
        web_pages_id (dict): _description_

    Returns:
        dict: _description_
    """
    last_ids = {}
    last_ids[comunity_names.andalucia] = save_andalucia(comunity_base_url.andalucia, web_pages_id[comunity_names.andalucia][range_id.start_id], web_pages_id[comunity_names.andalucia][range_id.end_id])
    last_ids[comunity_names.aragon] = save_aragon(comunity_base_url.aragon,  web_pages_id[comunity_names.aragon][range_id.start_id], web_pages_id[comunity_names.aragon][range_id.end_id])
    last_ids[comunity_names.extremadura] = save_extremadura(comunity_base_url.extremadura,  web_pages_id[comunity_names.extremadura][range_id.start_id], web_pages_id[comunity_names.extremadura][range_id.end_id])
    save_murcia(comunity_base_url.murcia)
    return last_ids


def update_ranges(web_pages_range: dict, last_ids: dict):
    """Update range id document.

    Args:
        web_pages_range (dict): _description_
        last_ids (dict): _description_
    """
    # Start range
    web_pages_range[comunity_names.andalucia][range_id.start_id] = last_ids[comunity_names.andalucia] + 1
    web_pages_range[comunity_names.aragon][range_id.start_id] = last_ids[comunity_names.aragon] + 1
    web_pages_range[comunity_names.extremadura][range_id.start_id] = last_ids[comunity_names.extremadura] + 1

    # End range
    web_pages_range[comunity_names.andalucia][range_id.end_id] = last_ids[comunity_names.andalucia] + 200
    web_pages_range[comunity_names.aragon][range_id.end_id] = last_ids[comunity_names.aragon] + 200
    web_pages_range[comunity_names.extremadura][range_id.end_id] = last_ids[comunity_names.extremadura] + 200


    # Write on json
    with open(web_pages_ids, "w") as f:
        json.dump(web_pages_range, f, indent=4)


def execute_scheduler():
    """Execute scheduler."""
    # Reading json range
    web_pages_range = read_webpages_ranges()

    # Saving data
    last_ids = save_data(web_pages_range)

    # Update ranges
    #update_ranges(web_pages_range, last_ids)



if __name__ == "__main__":
    execute_scheduler()
