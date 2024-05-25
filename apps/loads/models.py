from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.models import Customer, Operator, User
from config.core.choices import PRODUCT_STATUS_CHOICE, ON_WAY, STATUS_CHOICE, NOT_PAID
from config.models import BaseModel


class Product(BaseModel):
    status = models.CharField(choices=PRODUCT_STATUS_CHOICE, default=ON_WAY, max_length=10)
    barcode = models.CharField(max_length=155, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name='products',
                                 null=True, blank=True)
    accepted_by_china = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='products_china',
                                          null=True, blank=True)
    accepted_by_tashkent = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='products_tashkent',
                                             null=True, blank=True)
    accepted_time_china = models.DateTimeField(null=True, blank=True)
    accepted_time_tashkent = models.DateTimeField(null=True, blank=True)

    # photos file
    class Meta:
        db_table = 'Product'


class Load(BaseModel):
    loads_count = models.IntegerField(default=1)
    weight = models.FloatField()
    status = models.CharField(choices=STATUS_CHOICE, default=NOT_PAID, max_length=17)
    is_active = models.BooleanField(default=True)
    cost = models.FloatField(null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='loads')
    products = models.ManyToManyField(Product, related_name='loads')

    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='loads', null=True, blank=True)
    accepted_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "Load"
