from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import and_

from adapted_work.database.tables import Jobs


class DateFilter(BaseModel):
    start_date: Optional[datetime] = datetime(1900, 1, 1)
    end_date: Optional[datetime] = datetime.now()


def filter_by_date(date: DateFilter = None):
    """Filter from date"""
    if date is None:
        date = DateFilter()

    return and_(date.start_date <= Jobs.saved_date, date.end_date >= Jobs.saved_date)
