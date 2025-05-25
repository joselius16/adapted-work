from datetime import date
from typing import Any, Dict, List

from pydantic import BaseModel


class JobItem(BaseModel):
    """Job item."""

    title: str
    specialty: str
    link: str
    comunity: str
    disability_vacancies: str
    pred_disability: str
    date: date


class PaginatedResponse(BaseModel):
    """Paginated response."""

    items: List[JobItem]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_previous: bool
