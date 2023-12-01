from tortoise import fields
from common.models import AbstractModel


class People(AbstractModel):
    name = fields.CharField(max_length=120)
    job_description = fields.TextField()
    location = fields.CharField(max_length=120, null=True, blank=True)
    additional_data = fields.JSONField(null=True, blank=True)
    task = fields.ForeignKeyField(
        model_name='scraper.Tasks',
        related_name='tasks',
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = 'people'
