from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlmodel import Session, select

from adapted_work.database.connection import get_session
from adapted_work.database.tables import Comunity

router = APIRouter()


@router.get("/get_extremadura")
def get_all_extremadura(session: Session = Depends(get_session)):
    """Get data from Extremadura.

    Args:
        session (Session, optional): _description_. Defaults to Depends(get_session).

    Returns:
        _type_: _description_
    """
    logger.info("Getting Endalucia info")
    return session.exec(select(Comunity)).all()
