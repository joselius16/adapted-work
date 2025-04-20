from typing import Optional

from adapted_work.settings import database_settings

from sqlmodel import Field, SQLModel

class Comunity(SQLModel, table=True):
    __tablename__ = database_settings.TableName.comunity
    __table_args__ = {"schema": database_settings.schema.schema_database}
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    url: str = Field(default=None)


class Jobs(SQLModel, table=True):
    __tablename__ = database_settings.TableName.jobs
    __table_args__ = {"schema": database_settings.schema.schema_database}
    id: int = Field(default=None, primary_key=True)
    id_comunity: int = Field(foreign_key=f"{database_settings.schema.schema_database}.{database_settings.TableName.comunity}.id")
    ext_url: str
    disability_vacancies: Optional[str] = Field(default=None)
    dates: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    specialty: Optional[str] = Field(default=None)
    type_personnel: Optional[str] = Field(default=None)
    qualification : Optional[str] = Field(default=None)
    pred_disability : Optional[str] = Field(default=None)
    