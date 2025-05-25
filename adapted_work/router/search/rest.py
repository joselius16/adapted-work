import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlmodel import Session, select

from adapted_work.database.connection import get_session
from adapted_work.database.tables import Jobs
from adapted_work.router.search.extractor import (get_searched_data,
                                                  get_total_jobs)
from adapted_work.router.search.schema_model import PaginatedResponse
from adapted_work.settings import database_settings
from adapted_work.utils.sort_filters import order_by_filter

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
async def get_items(
    page: int,
    size: int,
    order: str,
    community: Optional[str] = None,
    session: Session = Depends(get_session),
):
    """Get jobs endpoint."""
    # Pages
    total = get_total_jobs(community, session)

    total_pages = math.ceil(total / size) if total > 0 else 1

    # Offset
    offset = (page - 1) * size

    order_by = order_by_filter(order)

    jobs = get_searched_data(size, offset, community, order_by, session)

    return PaginatedResponse(
        items=jobs,
        total=total,
        page=page,
        size=size,
        pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1,
    )
