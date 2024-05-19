from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import Customer
from config.core.choices import CAR_OR_AIR_CHOICE
from config.models import BaseModel


class Newsletter(BaseModel):
    is_gg = models.BooleanField(default=True)
    bot_type = models.CharField("user type", max_length=4, choices=CAR_OR_AIR_CHOICE)
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


class Delivery(BaseModel):
    TAKE_AWAY = 'TAKE_AWAY'
    YANDEX = 'YANDEX'
    DELIVERY_TYPE_CHOICE = [
        (TAKE_AWAY, _('Take away')),
        (YANDEX, _('Yandex')),
    ]
    delivery_type = models.CharField("delivery type", max_length=9, choices=DELIVERY_TYPE_CHOICE,
                                     null=True, blank=True)
    phone_number = models.CharField("phone number", max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Delivery'
