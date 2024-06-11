from django.db import models

from config.models import BaseModel


class OrderEMU(BaseModel):
    phone_number = models.CharField(max_length=30, null=True, blank=True)

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
