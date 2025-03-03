from fastapi import APIRouter

from adapted_work.router.comunities.andalucia.get_andalucia.rest import \
    router as get_all_andalucia
from adapted_work.router.comunities.aragon.get_aragon.rest import \
    router as get_all_aragon
from adapted_work.router.comunities.extremadura.get_extremadura.rest import \
    router as get_all_extremadura
from adapted_work.router.comunities.murcia.get_murcia.rest import \
    router as get_all_murcia

api_router = APIRouter()

api_router.include_router(get_all_andalucia, tags=["Andalucia"], prefix="/andalucia")
api_router.include_router(
    get_all_extremadura, tags=["Extremadura"], prefix="/extremadura"
)
api_router.include_router(get_all_aragon, tags=["Aragon"], prefix="/aragon")
api_router.include_router(get_all_murcia, tags=["Murcia"], prefix="/murcia")
