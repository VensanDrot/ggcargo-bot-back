from django.contrib.auth.models import AbstractUser
from django.db import models

from config.models import BaseModel


class User(AbstractUser):
    first_name = None
    last_name = None
    full_name = models.CharField("full name", max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'User'


class Customer(BaseModel):
    debt = models.FloatField(default=0)
    phone_number = models.CharField("phone number", max_length=35, null=True, blank=True)

    CAR = 'CAR'
    AIR = 'AIR'
    CAR_OR_AIR_CHOICE = [
        (CAR, 'Car'),
        (AIR, 'Air')
    ]
    user_type = models.CharField("user type", max_length=3, choices=CAR_OR_AIR_CHOICE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')

    class Meta:
        db_table = 'Customer'
