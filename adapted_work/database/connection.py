from loguru import logger
from sqlmodel import Session, SQLModel, create_engine, select, text

from adapted_work.database.tables import (  # 🔹 Importa los modelos aquí
    Comunity, ComunityType)
from adapted_work.settings import settings

engine = create_engine(settings.database_uri, echo=True)


def create_schema_if_not_exists(engine, schema=settings.schema_database):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        conn.commit()


create_schema_if_not_exists(engine)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def initialize_data():
    """Check if data exists."""
    try:
        with Session(engine) as session:
            existing = session.exec(
                select(ComunityType).where(
                    ComunityType.comunity_name.in_(
                        ["Andalucia", "Aragon", "Extremadura", "Murcia"]
                    )
                )
            ).all()

            if not existing:
                comunities = [
                    ComunityType(
                        comunity_name="Andalucia",
                        url_comunity="https://www.juntadeandalucia.es/",
                    ),
                    ComunityType(
                        comunity_name="Aragon",
                        url_comunity="https://aplicaciones.aragon.es/",
                    ),
                    ComunityType(
                        comunity_name="Extremadura",
                        url_comunity="https://www.juntaex.es/",
                    ),
                    ComunityType(
                        comunity_name="Murcia",
                        url_comunity="https://empleopublico.carm.es/",
                    ),
                ]
                session.add_all(comunities)
                session.commit()
                logger.info("Data inserted propertly.")
            else:
                logger.info("Data already inserted.")
    except:
        logger.error("Cannot execute initialize data.")
