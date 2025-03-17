from typing import Optional

from sqlmodel import Field, SQLModel

from adapted_work.settings import settings, table_names


class ComunityType(SQLModel, table=True):
    __tablename__ = table_names.comunity_type
    __table_args__ = {"schema": settings.schema_database}

    id: int = Field(default=None, primary_key=True)
    comunity_name: str
    url_comunity: str


class Comunity(SQLModel, table=True):
    __tablename__ = table_names.comunity
    __table_args__ = {"schema": settings.schema_database}

    id: int = Field(default=None, primary_key=True)
    id_comunity_type: int = Field(
        foreign_key=f"{settings.schema_database}.{table_names.comunity_type}.id"
    )
    ext_url: str
    dates: Optional[str] = None
    disability_vacancies: Optional[str] = None
    specialty: Optional[str] = None
    qualifycation: Optional[str] = None
    type_of_personnel: Optional[str] = None
