from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from scraper.routers import scraper_routers
from config.settings import ALLOW_ORIGINS, TORTOISE_ORM


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(router=scraper_routers)


def init_middleware() -> list[Middleware]:
    middlewares = [
        Middleware(
            CORSMiddleware,
            allow_origins=ALLOW_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
    return middlewares


def init_app():
    app_ = FastAPI(
        version='0.1.0',
        middleware=init_middleware(),
    )
    init_db(app=app_)
    init_routers(app=app_)

    return app_


app = init_app()
