from typing import Optional

from sqlmodel import Field, SQLModel


class Comunity(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    disability_vacancies: Optional[str] = None
    end_date: Optional[str] = None
