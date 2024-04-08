from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.models import BaseModel

username_validator = UnicodeUsernameValidator()


class CustomerID(BaseModel):
    code = models.CharField(max_length=255)

    class Meta:
        db_table = 'CustomerID'


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    first_name = None
    last_name = None
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True, blank=True
    )
    email = models.EmailField(_("email address"), unique=True)
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
    is_gg = models.BooleanField(default=True)
    passport_photo = models.FileField(null=True, blank=True)  # if user_type==AIR
    birt_date = models.DateField(null=True, blank=True)  # if user_type==AIR
    passport_serial_number = models.CharField(max_length=100, null=True, blank=True)  # if user_type==AIR

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    customer_code = models.ForeignKey(CustomerID, on_delete=models.CASCADE, related_name='customers')

    class Meta:
        db_table = 'Customer'


WEB = 'WEB'
TELEGRAM = 'TELEGRAM'
WEB_OR_TELEGRAM_CHOICE = [
    (WEB, 'Web'),
    (TELEGRAM, 'Telegram')
]
TASHKENT = 'TASHKENT'
CHINA = 'CHINA'
WAREHOUSE_CHOICE = [
    (TASHKENT, 'Tashkent'),
    (CHINA, 'China')
]


class Operator(BaseModel):
    # Type(Telegram / Web

    tg_id = models.CharField(max_length=155, null=True, blank=True)
    operator_type = models.CharField("operator type", max_length=8, choices=WEB_OR_TELEGRAM_CHOICE)
    warehouse = models.CharField("warehouse", max_length=8, choices=WAREHOUSE_CHOICE, null=True, blank=True)
    is_gg = models.BooleanField(default=True)
    # Ownership ? TODO: what is this
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operators')

    class Meta:
        db_table = 'Operator'
