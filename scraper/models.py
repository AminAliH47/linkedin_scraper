from tortoise import fields
from common.models import AbstractModel
import enum


class StateEnum(enum.Enum):
    SUCCESS = 'SUCCESS'
    PENDING = 'PENDING'
    FAILURE = 'FALIURE'


class Tasks(AbstractModel):
    task_id = fields.UUIDField(unique=True)
    state = fields.CharEnumField(StateEnum, default=StateEnum.PENDING)

    class Meta:
        table = 'tasks'


class ScrapData(AbstractModel):
    topic = fields.CharField(max_length=120)
    max_people = fields.IntField(default=20)
    task = fields.ForeignKeyField(
        model_name='scraper.Tasks',
        related_name='scrap_data',
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = 'scrap_data'
