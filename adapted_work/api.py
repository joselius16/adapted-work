from fastapi import APIRouter

from adapted_work.router.comunities.all.rest import router as get_comunities
from adapted_work.router.comunities.andalucia.get_andalucia.rest import \
    router as get_all_andalucia
from adapted_work.router.comunities.aragon.get_aragon.rest import \
    router as get_all_aragon
from adapted_work.router.comunities.extremadura.get_extremadura.rest import \
    router as get_all_extremadura
from adapted_work.router.comunities.murcia.get_murcia.rest import \
    router as get_all_murcia
from adapted_work.router.search.rest import router as search_jobs

api_router = APIRouter()

api_router.include_router(get_all_andalucia, tags=["Jobs"], prefix="/andalucia")
api_router.include_router(get_all_extremadura, tags=["Jobs"], prefix="/extremadura")
api_router.include_router(get_all_aragon, tags=["Jobs"], prefix="/aragon")
api_router.include_router(get_all_murcia, tags=["Jobs"], prefix="/murcia")
api_router.include_router(search_jobs, tags=["Jobs"], prefix="/search")
api_router.include_router(get_comunities, tags=["Communities"], prefix="/communities")
