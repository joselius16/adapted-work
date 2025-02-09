from sqlmodel import Session, SQLModel, create_engine

from adapted_work.settings import settings

engine = create_engine(settings.database_uri, echo=True)

# Build table if doesn't exists
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
