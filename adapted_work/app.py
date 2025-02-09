from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from adapted_work.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Adapted work")

    origins = ["*"]

    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True)

    app.include_router(router=api_router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
