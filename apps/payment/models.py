from django.db import models

from apps.user.models import Customer
from config.models import BaseModel


class Payment(BaseModel):
    SUCCESSFUL = 'SUCCESSFUL'
    DECLINED = 'DECLINED'
    STATUS_CHOICE = [
        (SUCCESSFUL, 'Successful'),
        (DECLINED, 'Declined'),
    ]
    status = models.CharField(choices=STATUS_CHOICE, max_length=10)
    paid_amount = models.FloatField(null=True, blank=True)  # if declined
    comment = models.TextField(null=True, blank=True)  # if declined
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

    class Meta:
        db_table = 'Payment'
