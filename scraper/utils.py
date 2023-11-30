from playwright.async_api import async_playwright

from scraper.services.linkedin import LinkedScraper


async def run_linkedin_scraper(topic: str, max_people: int):
    async with async_playwright() as playwright:
        linkedin_scraper = LinkedScraper(playwright=playwright)
        return await linkedin_scraper.run(topic, max_people)
