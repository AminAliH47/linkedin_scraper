import asyncio
from typing import Callable

from config import celery
from config.db import wrap_db_celery

from scraper.utils import run_linkedin_scraper


def async_to_sync(func: Callable, *args, **kwargs) -> None:
    asyncio.run(wrap_db_celery(func, *args, **kwargs))


@celery.task(serialize='json', bind=True)
def run_scraper(self, topic: str, max_people: int = 20):
    task_id = self.request.id
    return async_to_sync(run_linkedin_scraper, task_id, topic, max_people)
