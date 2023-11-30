from playwright.async_api import async_playwright

from config import celery
from scraper.services.linkedin import LinkedScraper
import json
import asyncio
from asgiref.sync import async_to_sync


async def x():
    l1 = [{'a': 1, 'b': 2, 'c': 3, }]
    return json.dumps(l1)


@celery.task(serialize='json')
def run_linkedin_scraper(topic: str, max_people: int = 20):
    # async with async_playwright() as playwright:
    #     linkedin_scraper = LinkedScraper(playwright=playwright)
    #     return await linkedin_scraper.run(topic, max_people)
    a = async_to_sync(x)
    return a
