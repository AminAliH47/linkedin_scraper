import asyncio
import json
import re

from bs4 import BeautifulSoup
from people.schemas import PeopleSchema
from people.models import People
from scraper.cookies import LINKEDIN_AUTHENTICATION_COOKIES
from scraper.models import Tasks, StateEnum
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
        people_list = await self._process()

        validated_people = [
            PeopleSchema(
                **person
            ) for person in people_list
        ]

        task, created = await Tasks.get_or_create(task_id=self.task_id)
        task.state = StateEnum.SUCCESS
        await task.save()

        people = [
            People(
                name=person.name,
                job_description=person.job_description,
                location=person.location,
                additional_data=person.additional_data,
                task=task,
            ) for person in validated_people
        ]
        await People.bulk_create(people)

        return json.dumps(people_list)

    async def _authenticate(self, username: str, password: str) -> None:
        logger.info('Authenticating ...')

        page = self.page

        try:
            await page.goto(f'{self.BASE_URL}uas/login/')
        except Error:
            await page.reload(timeout=60000)

        await asyncio.sleep(1)

        await page.context.add_cookies(LINKEDIN_AUTHENTICATION_COOKIES)

        await asyncio.sleep(1)

        await page.locator('#username').fill(username)
        await page.locator('#password').fill(password)
        await asyncio.sleep(1)
        await page.locator(
            '#organic-div > form > div.login__form_action_container > button'
        ).click()

    async def _process(self) -> list[dict]:
        # TODO: Async this logic
        people = []
        for page in range(1, 100):
            searched_people = await self._search_people(page)
            scraped_people = await self._scrap_people(searched_people)

            people.extend(scraped_people)

            if len(people) > self.max_people:
                break

        return people

    async def _search_people(self, page_num: int) -> str:
        page = self.page
        base_url = self.BASE_URL

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
            await page.reload(timeout=60000, wait_until='load')

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
