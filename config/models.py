from django.db import models
from django.utils.timezone import localtime


class LocalizedDateTimeField(models.DateTimeField):
    def to_python(self, value):
        value = super().to_python(value)
        value = localtime(value)
        return value


class BaseModel(models.Model):
    created_at = LocalizedDateTimeField(auto_now_add=True, null=True)
    updated_at = LocalizedDateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
