import asyncio
from scraper.base import BaseScraper
from config import envs
from playwright.async_api import Error
from scraper import xpaths


class LinkedScraper(BaseScraper):
    BASE_URL = envs.LINKEDIN_BASE_URL

    async def _authenticate(self, username: str, password: str) -> None:
        page = self.page

        await page.goto(f'{self.BASE_URL}/uas/login/')

        await page.locator('#username').fill(username)
        await page.locator('#password').fill(password)
        await page.locator(
            '#organic-div > form > div.login__form_action_container > button'
        ).click()

    async def _search_people(self, envelope: str) -> str | dict:
        page = self.page
        base_url = self.BASE_URL

        search_url = f'{base_url}search/results/people/?keywords={envelope}'

        await page.goto(search_url, wait_until='load')

        try:
            people_list = page.locator(xpaths.PEOPLE_LIST_XPATH)
        except Error:
            page.reload(wait_until='load')

            try:
                people_list = page.locator(xpaths.PEOPLE_LIST_XPATH)
            except Error:
                return 'No results'

        x = await people_list.inner_html()
        with open('index.html', 'x', encoding="utf-8") as file:
            file.write(str(x))

    async def run(self, envelope: str):
        self.page = await self._config_playwright()

        await self._authenticate(
            username=envs.LINKEDIN_USERNAME,
            password=envs.LINKEDIN_PASSWORD,
        )
        await asyncio.sleep(2)
        await self._search_people(envelope=envelope)

        await asyncio.sleep(10)
