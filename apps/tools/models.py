from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.files.models import File
from apps.integrations.models import RegionEMU
from apps.loads.models import Load
from apps.user.models import Customer
from config.core.choices import CAR_OR_AIR_CHOICE, DELIVERY_TYPE_CHOICE, TAKE_AWAY, NEWSLETTER_STATUS_CHOICE, \
    NEWSLETTER_PENDING, EMU_SERVICE_CHOICE, TO_RECEIVER
from config.models import BaseModel


class Newsletter(BaseModel):
    bot_type = models.CharField("user type", max_length=4, choices=CAR_OR_AIR_CHOICE)
    send_date = models.DateTimeField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    photo_uz = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True, related_name='newsletter_uz')
    text_ru = models.TextField(null=True, blank=True)
    photo_ru = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True, related_name='newsletter_ru')

    status = models.CharField(choices=NEWSLETTER_STATUS_CHOICE, max_length=7, default=NEWSLETTER_PENDING)

    class Meta:
        db_table = 'Newsletter'


class Delivery(BaseModel):
    delivery_type = models.CharField("delivery type", max_length=9, choices=DELIVERY_TYPE_CHOICE,
                                     default=TAKE_AWAY)
    phone_number = models.CharField("phone number", max_length=30, null=True, blank=True)
    town = models.ForeignKey(RegionEMU, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    address = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    telegram_message_id = models.IntegerField(null=True, blank=True)

    service_type = models.IntegerField(choices=EMU_SERVICE_CHOICE, default=TO_RECEIVER, null=True, blank=True)
    track_link = models.URLField(null=True, blank=True)
    message_sent = models.BooleanField(default=False)

    load = models.OneToOneField(Load, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='deliveries')

    class Meta:
        db_table = 'Delivery'
