import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from celery.result import AsyncResult
from auth.schemas import UserPydantic

from auth.utils import AuthSystem
from people.models import People
from people.schemas import PeoplePydanticList
from scraper.tasks import run_scraper


v1_routers = APIRouter()

auth = AuthSystem()


@v1_routers.get('/linkedin')
async def scrape_linkedin(topic: str, max_people: int = 20):
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


    print(user)

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
