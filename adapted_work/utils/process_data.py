from loguru import logger
from sqlmodel import Session, select

from adapted_work.database.connection import engine
from adapted_work.database.tables import Comunity, Jobs


def save_into_database(data_administration):
    try:
        logger.info("Saving into database.")
        with Session(engine) as session:
            for data in data_administration:
                statement = select(Jobs).where(Jobs.ext_url == data.ext_url)
                result = session.exec(statement).first()

                if result:
                    logger.info(f"Url {data.url} already in database.")
                    continue

                session.add(data)
                logger.info(f"saving: {data.ext_url}")
            session.commit()

        logger.info("Executed succesfully.")

    except Exception as e:
        logger.error(f"Cannot save into database: {e}")
