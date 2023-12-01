from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Query
from celery.result import AsyncResult
from auth.schemas import UserPydantic

from auth.utils import AuthSystem
from people.models import People
from people.schemas import PeoplePydanticList
from scraper.models import Tasks
from scraper.tasks import run_scraper


v1_routers = APIRouter()

auth = AuthSystem()


@v1_routers.get('/linkedin')
async def scrape_linkedin(
    topic: Annotated[str, Query(max_length=120)],
    max_people: Annotated[int, Query(le=999)] = 20,
    user: UserPydantic = Depends(auth.get_current_user),
):
    task = run_scraper.apply_async(
        kwargs={'max_people': max_people, 'topic': topic}
    )

    return {
        'status': 'Linkedin scraper is running',
        'task_id': task.id,
    }


@v1_routers.get("/result/{task_id}")
async def get_scraper_result(
    task_id: uuid.UUID,
    user: UserPydantic = Depends(auth.get_current_user),
):
    result = AsyncResult(str(task_id))

    # TODO: Add pagination in this endpoint
    people = People.filter(task__task_id=str(task_id))
    if await people.exists():
        people_json = await PeoplePydanticList.from_queryset(people)

        return {'people': people_json.model_dump(
            mode='json',
            exclude={'deleted_at', 'is_deleted', 'updated_at'},
        )}

    if result.state == 'PENDING':
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail='Scraper working...',
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task failed or does not exists ...'
        )


@v1_routers.get("/heartbeat")
async def scraper_heartbeat():
    await Tasks.first()
    return 'OK'
