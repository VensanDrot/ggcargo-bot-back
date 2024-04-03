from django.db import models

from apps.user.models import Customer
from config.models import BaseModel


class Product(BaseModel):
    barcode = models.CharField(max_length=155)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)

    # photos file
    class Meta:
        db_table = 'Product'


class Load(BaseModel):
    weight = models.FloatField()
    CREATED = 'CREATED'
    PAID = 'PAID'
    DONE = 'DONE'
    DONE_MAIL = 'DONE_MAIL'
    STATUS_CHOICE = [
        (CREATED, 'Created'),
        (PAID, 'Paid'),
        (DONE, 'Done'),
        (DONE_MAIL, 'Done-mail'),
    ]
    status = models.CharField(choices=STATUS_CHOICE, default=CREATED, max_length=9)

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='loads')
    products = models.ManyToManyField(Product, related_name='loads')

    class Meta:
        db_table = "Load"
