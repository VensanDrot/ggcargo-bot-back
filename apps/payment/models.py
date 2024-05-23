from django.db import models

from apps.loads.models import Load
from apps.user.models import Customer, User
from config.models import BaseModel


class Payment(BaseModel):
    SUCCESSFUL = 'SUCCESSFUL'
    DECLINED = 'DECLINED'
    STATUS_CHOICE = [
        (SUCCESSFUL, 'Successful'),
        (DECLINED, 'Declined'),
    ]
    status = models.CharField(choices=STATUS_CHOICE, max_length=10, null=True, blank=True)
    paid_amount = models.FloatField(null=True, blank=True)  # on moderation
    comment = models.TextField(null=True, blank=True)  # if declined

    CASH = 'CASH'
    CARD = 'CARD'
    PAYMENT_TYPE_CHOICE = [
        (CASH, CASH),
        (CARD, CARD),
    ]
    payment_type = models.CharField(max_length=5, choices=PAYMENT_TYPE_CHOICE, null=True, blank=True)
    is_operator = models.BooleanField(default=False)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    load = models.ForeignKey(Load, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

    class Meta:
        db_table = 'Payment'
