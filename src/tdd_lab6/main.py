from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware

from tdd_lab6.models import Item
from tdd_lab6.routers import include_routers
from tdd_lab6.settings import Settings
from .exceptions import add_exception_handlers


@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    await init_beanie(
        database=app.mongo_client[app.settings.mongo.DATABASE],
        document_models=[Item],
    )

    yield


def create_app(settings: Settings) -> FastAPI:
    mongo_client = AsyncIOMotorClient(settings.mongo.url)

    app = FastAPI(lifespan=fastapi_lifespan)

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.settings = settings
    app.mongo_client = mongo_client

    include_routers(app)
    add_exception_handlers(app)

    return app


def main() -> FastAPI:
    settings = Settings()

    app = create_app(settings)

    return app
