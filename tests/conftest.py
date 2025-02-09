import pytest
from sqlmodel import Session, SQLModel, create_engine
from testcontainers.postgres import PostgresContainer

from adapted_work.database.tables import \
    Andalucia  # Asegúrate de que la importación es correcta


@pytest.fixture(scope="session")
def postgres_container():
    """Levanta un contenedor de PostgreSQL para pruebas y lo cierra después de la sesión."""
    with PostgresContainer("postgres:15") as postgres:
        postgres.start()
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    """Crea el motor de SQLAlchemy apuntando al contenedor de PostgreSQL."""
    db_url = postgres_container.get_connection_url()
    engine = create_engine(db_url)

    # 🔹 CREAR LAS TABLAS SI NO EXISTEN
    SQLModel.metadata.create_all(engine)

    return engine


@pytest.fixture(scope="function")
def db_session(engine):
    """Crea una sesión de base de datos para cada test."""
    with Session(engine) as session:
        yield session
        session.rollback()  # Limpia la base de datos después de cada test
