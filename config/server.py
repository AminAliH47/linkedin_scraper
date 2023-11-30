from fastapi import FastAPI
from fastapi.middleware import Middleware

from scraper.routers import scraper_routers


def init_routers(app: FastAPI) -> None:
    app.include_router(router=scraper_routers)


def init_middleware() -> list[Middleware]:
    ...


def init_app():
    app_ = FastAPI(
        version='0.1.0',
        middleware=init_middleware(),
    )
    init_routers(app=app_)

    return app_


app = init_app()
