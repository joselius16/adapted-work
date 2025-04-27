from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlmodel import Session, select

from adapted_work.database.connection import get_session
from adapted_work.database.tables import Jobs
from adapted_work.settings import database_settings

router = APIRouter()


@router.get("/get_aragon")
def get_all_aragon(session: Session = Depends(get_session)):
    """Get data from Aragon.

    Args:
        session (Session, optional): _description_. Defaults to Depends(get_session).

    Returns:
        _type_: _description_
    """
    try:
        logger.info("Getting aragon info")
        return session.exec(
            select(Jobs).where(Jobs.id_comunity == database_settings.comunity_id.aragon)
        ).all()
    except Exception as e:
        logger.error(f"Error executing aragon endpoint: {e}")
        raise HTTPException(status_code=404)
