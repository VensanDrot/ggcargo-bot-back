from django.db import models

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
