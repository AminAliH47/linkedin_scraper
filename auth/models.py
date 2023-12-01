from tortoise import fields

from common.models import AbstractModel


class Users(AbstractModel):
    username = fields.CharField(max_length=20, unique=True, index=True)
    email = fields.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    password = fields.CharField(max_length=255)

    class Meta:
        table = 'users'
