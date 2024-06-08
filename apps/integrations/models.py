from django.db import models

from config.models import BaseModel


class OrderEMU(BaseModel):
    phone_number = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'OrderEMU'
