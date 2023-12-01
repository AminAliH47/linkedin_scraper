from playwright.async_api import async_playwright

from scraper.services.linkedin import LinkedScraper
from scraper.models import Tasks, ScrapData


async def run_linkedin_scraper(task_id, topic: str, max_people: int):
    async with async_playwright() as playwright:
        task = await Tasks.create(task_id=task_id)
        await ScrapData.create(topic=topic, max_people=max_people, task=task)

        linkedin_scraper = LinkedScraper(playwright=playwright)
        return await linkedin_scraper.run(
            task_id=task_id,
            topic=topic,
            max_people=max_people,
        )
