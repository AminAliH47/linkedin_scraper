from fastapi import FastAPI
from fastapi.middleware import Middleware


def init_routers(app: FastAPI) -> list:
    ...


def init_middleware() -> list[Middleware]:
    ...


def init_app():
    app_ = FastAPI(
        version='0.1.0',
        routers=init_routers(),
        middleware=init_middleware(),
    )

    return app_


app = init_app()
