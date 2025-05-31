from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from adapted_work.settings import database_settings


class Community(SQLModel, table=True):
    __tablename__ = database_settings.TableName.community
    __table_args__ = {"schema": database_settings.schema.schema_database}
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    code: str = Field(default=None)
    url: str = Field(default=None)


class Jobs(SQLModel, table=True):
    __tablename__ = database_settings.TableName.jobs
    __table_args__ = {"schema": database_settings.schema.schema_database}
    id: int = Field(default=None, primary_key=True)
    id_community: int = Field(
        foreign_key=f"{database_settings.schema.schema_database}.{database_settings.TableName.community}.id",
        description="Community id",
    )
    ext_url: str = Field(description="Url from posted job")
    disability_vacancies: Optional[str] = Field(
        default=None, description="Number of disability vacancies"
    )
    dates: Optional[str] = Field(
        default=None, description="Dates from job applications"
    )
    saved_date: Optional[datetime] = Field(
        default=None, description="Day when the job is saved"
    )
    title: Optional[str] = Field(default=None, description="Job's title")
    specialty: Optional[str] = Field(default=None, description="Job's spectialty")
    type_personnel: Optional[str] = Field(default=None, description="Type of personnel")
    qualification: Optional[str] = Field(
        default=None, description="Qualification needed"
    )
    pred_disability: Optional[str] = Field(
        default=None, description="Type of disabilities predicted for the job"
    )
