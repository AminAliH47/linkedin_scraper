from abc import ABC

from playwright.async_api import Playwright, Page


class BaseScraper(ABC):
    def __init__(self, playwright: Playwright):
        self.playwright = playwright

    async def _config_playwright(self) -> Page:
        playwright = self.playwright
        browser = await playwright.firefox.launch(headless=True)
        return await browser.new_page()

    async def _authenticate(self, username: str, password: str):
        ...

    async def run(self, topic: str, *args, **kwargs):
        self.page = await self._config_playwright()
        self.topic = topic

        return await self._run(*args, **kwargs)