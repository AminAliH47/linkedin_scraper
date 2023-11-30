from config import celery
from asgiref.sync import async_to_sync

from scraper.utils import run_linkedin_scraper


@celery.task(serialize='json')
def run_scraper(topic: str, max_people: int = 20):
    return async_to_sync(run_linkedin_scraper)(topic, max_people)
