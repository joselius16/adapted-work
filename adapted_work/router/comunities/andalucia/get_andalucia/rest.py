from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlmodel import Session, and_, select

from adapted_work.database.connection import get_session
from adapted_work.database.tables import Jobs
from adapted_work.settings import database_settings
from adapted_work.utils.sort_filters import DateFilter, filter_by_date

router = APIRouter()


@router.get("/get_andalucia")
def get_all_andalucia(session: Session = Depends(get_session)):
    """Get data from andalucia.

    Args:
        session (Session, optional): _description_. Defaults to Depends(get_session).

    Returns:
        _type_: _description_
    """
    try:
        logger.info("Getting andalucia info")
        return session.exec(
            select(Jobs).where(
                Jobs.id_community == database_settings.community_id.andalucia
            )
        ).all()
    except Exception as e:
        logger.error(f"Error executing andalucia endpoint: {e}")
        raise HTTPException(status_code=404)
