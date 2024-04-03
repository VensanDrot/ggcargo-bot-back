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
        db_table = 'Cost'


class ChannelLink(Settings):
    link = models.TextField()

    class Meta:
        db_table = 'ChannelLink'


class WarehouseAddress(Settings):
    link = models.TextField()

    class Meta:
        db_table = 'WarehouseAddress'


class Newsletter(BaseModel):
    is_gg = models.BooleanField(default=True)
    CAR = 'CAR'
    AIR = 'AIR'
    CAR_OR_AIR_CHOICE = [
        (CAR, 'Car'),
        (AIR, 'Air')
    ]
    bot_type = models.CharField("user type", max_length=3, choices=CAR_OR_AIR_CHOICE)
    text_uz = models.TextField(null=True, blank=True)
    photo_uz = models.FileField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    photo_ru = models.FileField(null=True, blank=True)
    SENT = 'SENT'
    PENDING = 'PENDING'
    STATUS_CHOICE = [
        (SENT, 'Sent'),
        (PENDING, 'Pending')
    ]
    status = models.CharField(choices=STATUS_CHOICE, max_length=7, default=PENDING)

    class Meta:
        db_table = 'Newsletter'
