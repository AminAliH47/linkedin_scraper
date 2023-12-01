from tortoise import Model, fields


class AbstractModel(Model):
    id = fields.BigIntField(pk=True, editable=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True, blank=True)
    is_deleted = fields.BooleanField(default=False)

    class Meta:
        abstract = True
