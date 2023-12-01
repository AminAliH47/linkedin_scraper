from config.envs import envs
from celery import Celery

celery = Celery(
    'tasks',
    broker=envs.CELERY_BROKER_URL,
    backend=envs.CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=True,
    include=['scraper.tasks']
)
