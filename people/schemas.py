from pydantic import BaseModel
from tortoise.contrib.pydantic import (
    pydantic_model_creator,
    pydantic_queryset_creator,
)
from people.models import People


class PeopleSchema(BaseModel):
    name: str
    job_description: str
    location: str | None = None
    additional_data: dict | None = None


PeoplePydantic = pydantic_model_creator(People)
PeoplePydanticList = pydantic_queryset_creator(
    People,
    exclude={'is_deleted', 'deleted_at', 'updated_at'}
)
