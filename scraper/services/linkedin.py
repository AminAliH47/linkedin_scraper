# import asyncio
import asyncio
import json
import re

from bs4 import BeautifulSoup
from scraper.services.base import BaseScraper
from config import envs, logger
from playwright.async_api import Error
from scraper.services import xpaths


class LinkedScraper(BaseScraper):
    BASE_URL = envs.LINKEDIN_BASE_URL

    async def _run(self, *args, **kwargs):
        self.max_people = kwargs.get('max_people', 20)

        await self._authenticate(
            username=envs.LINKEDIN_USERNAME,
            password=envs.LINKEDIN_PASSWORD,
        )

        return await self._process()

    async def _authenticate(self, username: str, password: str) -> None:
        logger.info('Authenticating ...')

        page = self.page

        await page.goto(f'{self.BASE_URL}uas/login/')

        await page.context.add_cookies(
            [{'name': 'lang', 'value': 'v=2&lang=en-us', 'domain': '.linkedin.com', 'path': '/', 'expires': -1,
              'httpOnly': False, 'secure': True, 'sameSite': 'None'},
             {'name': 'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg',
              'value': '-637568504%7CMCIDTS%7C19692%7CvVersion%7C5.1.1', 'domain': '.linkedin.com', 'path': '/',
              'expires': 1716925538, 'httpOnly': False, 'secure': False, 'sameSite': 'None'},
             {'name': 'li_rm',
              'value':
              'AQEGC1VEnJ3aKAAAAYwhw-ZHcWHlG1Smy8hw1HvCSV6ZiONzUoL6m6zM7iPiJ7a9_y2sqjNSDUcXnGyP06SZzOd46I-6yv1jeCSFkpIMO12C-Ym_F4UBYbiH',
              'domain': '.www.linkedin.com', 'path': '/', 'expires': 1732909539, 'httpOnly': True, 'secure': True,
              'sameSite': 'None'},
             {'name': 'li_at',
              'value':
              'AQEDATSvI-sB0g-7AAABjCHD9XYAAAGMRdB5dk0AP-3BnTPyX5KK-0rcqwrSBXZaI08sFByO6TCehIhabnYm_JnERhmlmEa7LgH0w3yJZtXRi875TRDzVbs89L7DRKZk51EiJ9_ADn8U1PIWUDnuO-c9',
              'domain': '.www.linkedin.com', 'path': '/', 'expires': 1732909539, 'httpOnly': True, 'secure': True,
              'sameSite': 'None'},
             {'name': 'liap', 'value': 'true', 'domain': '.linkedin.com', 'path': '/', 'expires': 1709149539,
              'httpOnly': False, 'secure': True, 'sameSite': 'None'},
             {'name': 'JSESSIONID', 'value': '"ajax:0782053775527920009"', 'domain': '.www.linkedin.com', 'path': '/',
              'expires': 1709149539, 'httpOnly': False, 'secure': True, 'sameSite': 'None'},
             {'name': 'bcookie', 'value': '"v=2&2ea2e7f0-d15b-4a98-8132-9658e6f6849c"', 'domain': '.linkedin.com',
              'path': '/', 'expires': 1732909539, 'httpOnly': False, 'secure': True, 'sameSite': 'None'},
             {'name': 'bscookie',
              'value': '"v=1&2023113019453520bfbe87-9af8-4c05-8a78-8fb43baae038AQHHqeVTx4KRYr37X7mTYb7vQgO5av1u"',
              'domain': '.www.linkedin.com', 'path': '/', 'expires': 1732909539, 'httpOnly': True, 'secure': True,
              'sameSite': 'None'},
             {'name': 'lidc',
              'value':
              '"b=VB27:s=V:r=V:a=V:p=V:g=5428:u=147:x=1:i=1701373540:t=1701375200:v=2:sig=AQFT0oDXq8s1OM30AvkUAkgpL4c0FK8f"',
              'domain': '.linkedin.com', 'path': '/', 'expires': 1701375200, 'httpOnly': False, 'secure': True,
              'sameSite': 'None'}])

        await asyncio.sleep(2)

        # c = await page.context.cookies()
        # print(c)

        await page.locator('#username').fill(username)
        await page.locator('#password').fill(password)
        await page.locator(
            '#organic-div > form > div.login__form_action_container > button'
        ).click()

        # sign_in_button = page.locator('.main__sign-in-link')
        # if await sign_in_button.count() <= 0:
        #     return

        # await sign_in_button.click()

        # await page.locator('#username').fill(username)
        # await page.locator('#password').fill(password)
        # await page.locator(
        #     '#organic-div > form > div.login__form_action_container > button'
        # ).click()

    async def _process(self) -> list[dict]:
        # TODO: Async this logic
        people = []
        for page in range(1, 100):
            searched_people = await self._search_people(page)
            scraped_people = await self._scrap_people(searched_people)

            people.extend(scraped_people)

            if len(people) > self.max_people:
                break

        return json.dumps(people)

    async def _search_people(self, page_num: int) -> str:
        page = self.page
        base_url = self.BASE_URL

        c = await page.context.cookies()
        print(c, '==== searching')

        logger.info(f'Searching at page: {page_num}')

        search_url = (
            f'{base_url}search/results/people/'
            f'?keywords={self.topic}&page={page_num}'
        )

        await page.goto(search_url, wait_until='domcontentloaded')
        await asyncio.sleep(2)

        try:
            people_list = await page.locator(
                xpaths.PEOPLE_LIST_XPATH
            ).inner_html()
        except Error:
            page.reload(wait_until='load')

            try:
                people_list = await page.locator(
                    xpaths.PEOPLE_LIST_XPATH
                ).inner_html()
            except Error:
                return 'No results'

        return people_list

    async def _scrap_people(self, searched_people: str):
        logger.info('Scrapping people')

        soup = BeautifulSoup(searched_people, 'html.parser')

        people = []

        people_container = soup.find_all(
            'li',
            class_='reusable-search__result-container',
        )
        for container in people_container:
            job_description = container.find(
                'div', class_='entity-result__primary-subtitle'
            ).text.strip()

            try:
                summary = container.find(
                    'p', class_='entity-result__summary'
                ).text.strip()
            except AttributeError:
                summary = ''

            if (
                bool(re.search(self.topic, job_description, re.I)) or
                bool(re.search(self.topic, summary, re.I))
            ):
                name = container.find(
                    'span', class_='entity-result__title-text'
                ).find('span', attrs={'aria-hidden': 'true'}).text.strip()

                try:
                    location = container.find(
                        'div', class_='entity-result__secondary-subtitle'
                    ).text.strip()
                except AttributeError:
                    location = ''

                people.append({
                    'name': name,
                    'job_description': job_description,
                    'location': location,
                })

        return people
