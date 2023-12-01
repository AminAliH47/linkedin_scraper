from typing import Callable
from tortoise import Tortoise

from config import envs

DB_URL = (f'postgres://{envs.POSTGRES_USER}:{envs.POSTGRES_PASSWORD}'
          f'@{envs.POSTGRES_HOST}:{envs.POSTGRES_PORT}/{envs.POSTGRES_DB}')


async def connect_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={
            'models': [
                'aerich.models',
                'people.models',
            ],
            'scraper': [
                'scraper.models',
            ]
        }
    )
    await Tortoise.generate_schemas()


async def disconnect_db():
    await Tortoise.close_connections()


async def wrap_db_celery(func: Callable, *args, **kwargs) -> None:
    try:
        await connect_db()
        await func(*args, **kwargs)
    finally:
        await disconnect_db()
