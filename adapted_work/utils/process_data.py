from loguru import logger
from sqlmodel import Session, select

from adapted_work.database.connection import engine
from adapted_work.database.tables import Comunity


def save_into_database(data_administration):
    try:
        logger.info("Saving into database.")
        with Session(engine) as session:
            for data in data_administration:
                statement = select(Comunity).where(Comunity.url == data.url)
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
