import uuid
from fastapi import APIRouter, HTTPException, status
from celery.result import AsyncResult
from scraper.tasks import run_scraper

v1_routers = APIRouter()


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
async def get_scraper_result(task_id: uuid.UUID):
    result = AsyncResult(str(task_id))

    print(result.state)
    if result.ready():
        return {"people": result.result}
    else:
        return HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail='Scrapping'
        )
