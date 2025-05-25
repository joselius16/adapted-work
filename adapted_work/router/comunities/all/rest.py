import math
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlmodel import Session, select

from adapted_work.database.connection import get_session
from adapted_work.database.tables import Jobs
from adapted_work.router.comunities.all.extractor import (get_comunities,
                                                          parse_comunities)
from adapted_work.settings import database_settings

router = APIRouter()


@router.get("/")
async def get_items(session: Session = Depends(get_session)):
    """Get all jobs."""
    comunities = get_comunities(session)
    parsed_comunities = parse_comunities(comunities)
    return parsed_comunities
