from django.db import models

from config.models import BaseModel


class Settings(BaseModel):
    is_gg = models.BooleanField(default=True, null=True, blank=True)
    CAR = 'CAR'
    AIR = 'AIR'
    CAR_OR_AIR_CHOICE = [
        (CAR, 'Car'),
        (AIR, 'Air')
    ]
    car_or_air = models.CharField(max_length=3, null=True, blank=True, choices=CAR_OR_AIR_CHOICE)

    class Meta:
        abstract = True


class PaymentCard(Settings):
    card_number = models.CharField(max_length=16)

    class Meta:
        db_table = 'PaymentCard'


class Cost(Settings):
    cost_per_kg = models.FloatField()

    class Meta:
        db_table = 'PaymentCard'


class ChannelLink(Settings):
    link = models.TextField()

    class Meta:
        db_table = 'ChannelLink'


class WarehouseAddress(Settings):
    link = models.TextField()

    class Meta:
        db_table = 'WarehouseAddress'


class Product(BaseModel):
    barcode = models.CharField(max_length=155)
    customer_id = models.CharField(max_length=155)

    # photos file
    class Meta:
        db_table = 'Product'
