from typing import Callable
from tortoise import Tortoise

from config import settings


async def connect_db():
    await Tortoise.init(config=settings.TORTOISE_ORM)


async def disconnect_db():
    await Tortoise.close_connections()


async def wrap_db_celery(func: Callable, *args, **kwargs) -> None:
    try:
        await connect_db()
        await func(*args, **kwargs)
    finally:
        await disconnect_db()
