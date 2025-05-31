from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlmodel import Session, and_, select

from adapted_work.database.connection import get_session
from adapted_work.database.tables import Jobs
from adapted_work.settings import database_settings
from adapted_work.utils.sort_filters import DateFilter, filter_by_date

router = APIRouter()


@router.post("/get_andalucia")
def get_all_andalucia(
    filter: DateFilter = None, session: Session = Depends(get_session)
):
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
                and_(
                    Jobs.id_community == database_settings.community_id.andalucia,
                    filter_by_date(filter),
                )
            )
        ).all()
    except Exception as e:
        logger.error(f"Error executing andalucia endpoint: {e}")
        raise HTTPException(status_code=404)
