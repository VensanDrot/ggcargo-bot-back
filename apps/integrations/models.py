import uuid

from django.db import models

from apps.loads.models import Load
from apps.user.models import Customer
from config.core.choices import EMU_SERVICE_CHOICE
from config.models import BaseModel


class OrderEMU(BaseModel):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    town = models.CharField(max_length=55, null=True, blank=True)
    service = models.IntegerField(choices=EMU_SERVICE_CHOICE, null=True, blank=True)

    tracking_link = models.URLField(null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    load = models.ForeignKey(Load, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'OrderEMU'


class RegionEMU(BaseModel):
    district_en = models.CharField(max_length=255, null=True, blank=True)
    district_ru = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    emu_city = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=155, null=True, blank=True)

    class Meta:
        db_table = 'RegionEMU'
