from loguru import logger
from sqlmodel import Session, SQLModel, create_engine, select, text

from adapted_work.database.tables import Community
from adapted_work.settings import settings

engine = create_engine(settings.database_uri, echo=True)


def get_session():
    """Get session."""
    with Session(engine) as session:
        yield session


def ensure_schema_exists(schema_name: str):
    """Check if the schema exists in database."""
    with Session(engine) as session:
        session.exec(
            text(
                f"""
                CREATE SCHEMA IF NOT EXISTS "{schema_name}";
            """
            )
        )
        session.commit()

    # Build tables if doesn't exists
    SQLModel.metadata.create_all(engine)


def initialize_data():
    """Check if data exists in database, otherwise, build it."""
    try:
        with Session(engine) as session:
            # Verify if data exists
            result = session.exec(
                select(Community).where(
                    Community.name.in_(["Andalucia", "Aragon", "Extremadura", "Murcia"])
                )
            )
            existing = result.all()

            if not existing:
                logger.info("Inserting data into community table")
                comunities = [
                    Community(
                        name="Andalucia",
                        code="AN",
                        url="https://www.juntadeandalucia.es",
                    ),
                    Community(name="Aragon", code="AR", url="https://www.aragon.es"),
                    Community(
                        name="Extremadura", code="EX", url="https://www.juntaex.es"
                    ),
                    Community(
                        name="Murcia", code="MU", url="https://empleopublico.carm.es"
                    ),
                ]
                session.add_all(comunities)
                session.commit()
                logger.info("Data inserted.")
    except Exception as e:
        logger.error(f"Cannot insert data: {e}")
