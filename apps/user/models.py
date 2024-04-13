from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.models import BaseModel

username_validator = UnicodeUsernameValidator()

# CUSTOMERS
AUTO = 'AUTO'
AVIA = 'AVIA'
CAR_OR_AIR_CHOICE = [
    (AUTO, _('Auto')),
    (AVIA, _('Avia'))
]
GG = 'GG'
EXP = 'EXP'
COMPANY_TYPE_CHOICES = [
    (GG, GG),
    (EXP, EXP),
]
# OPERATORS
WEB = 'WEB'
TELEGRAM = 'TELEGRAM'
WEB_OR_TELEGRAM_CHOICE = [
    (WEB, _('Web')),
    (TELEGRAM, _('Telegram'))
]
TASHKENT = 'TASHKENT'
CHINA = 'CHINA'
WAREHOUSE_CHOICE = [
    (TASHKENT, _('Tashkent')),
    (CHINA, _('China'))
]


class User(AbstractUser):
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
    company_type = models.CharField(_("company type"), max_length=155, choices=COMPANY_TYPE_CHOICES, default=GG)

    class Meta:
        db_table = 'User'


class Customer(BaseModel):
    code = models.CharField(max_length=255, unique=True)
    debt = models.FloatField(default=0)
    phone_number = models.CharField(_("phone number"), max_length=35, null=True, blank=True)

    user_type = models.CharField(_("user type"), max_length=4, choices=CAR_OR_AIR_CHOICE)
    passport_photo = models.FileField(null=True, blank=True)  # if user_type==AIR
    birt_date = models.DateField(null=True, blank=True)  # if user_type==AIR
    passport_serial_number = models.CharField(max_length=100, null=True, blank=True)  # if user_type==AIR
    products_accepted = models.IntegerField(default=0)
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='customers_accepted_by',
                                    null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')

    class Meta:
        db_table = 'Customer'


class Operator(BaseModel):
    # Type(Telegram / Web

    tg_id = models.CharField(max_length=155, null=True, blank=True)
    operator_type = models.CharField(_("operator type"), max_length=8, choices=WEB_OR_TELEGRAM_CHOICE)
    warehouse = models.CharField(_("warehouse"), max_length=8, choices=WAREHOUSE_CHOICE, null=True, blank=True)
    # Ownership ? TODO: what is this
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='operator')

    class Meta:
        db_table = 'Operator'
