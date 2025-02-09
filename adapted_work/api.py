from fastapi import APIRouter

from adapted_work.router.comunities.andalucia.get_andalucia.rest import \
    router as get_all_andalucia

api_router = APIRouter()

api_router.include_router(get_all_andalucia, tags=["Andalucia"], prefix="/andalucia")
