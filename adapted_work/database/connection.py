from sqlmodel import Session, SQLModel, create_engine, select, text
from adapted_work.database.tables import Comunity

from adapted_work.settings import settings
from loguru import logger

engine = create_engine(settings.database_uri, echo=True)

def get_session():
    """Get session."""
    with Session(engine) as session:
        yield session

def ensure_schema_exists(schema_name: str):
    """Check if the schema exists in database."""
    with Session(engine) as session:
        session.exec(
            text(f"""
                CREATE SCHEMA IF NOT EXISTS "{schema_name}";
            """)
        )
        session.commit()

    # Build tables if doesn't exists
    SQLModel.metadata.create_all(engine)

def initialize_data():
    """Check if data exists in database, otherwise, build it."""
    with Session(engine) as session:
        # Verify if data exists
        result = session.exec(select(Comunity).where(Comunity.name.in_(
            ["Andalucia", "Aragon", "Extremadura", "Murcia"]
        )))
        existing = result.all()

        if not existing:
            logger.info("Inserting data into comunity table")
            comunities = [
                Comunity(name="Andalucia", url = 'https://www.juntadeandalucia.es'),
                Comunity(name="Aragon", url= 'https://www.aragon.es'),
                Comunity(name="Extremadura", url = 'https://www.juntaex.es'),
                Comunity(name="Murcia", url = 'https://empleopublico.carm.es'),
            ]
            session.add_all(comunities)
            session.commit()
            logger.info("Data inserted.")
        else:
            logger.error("Cannot insert data.")