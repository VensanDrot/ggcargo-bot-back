from django.db import models

from config.models import BaseModel


class File(BaseModel):
    name = models.CharField(max_length=300, null=True)
    gen_name = models.CharField(max_length=100, null=True)
    size = models.FloatField(null=True)
    path = models.TextField(null=True)
    content_type = models.CharField(max_length=100, null=True)
    extension = models.CharField(max_length=30, null=True)
    china_product = models.ForeignKey("loads.Product", on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='china_files')
    loads = models.ForeignKey("loads.Load", on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='files')
    payments = models.ForeignKey("payment.Payment", on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='files')
    customer_registration = models.ForeignKey("user.CustomerRegistration", on_delete=models.SET_NULL,
                                              null=True, blank=True, related_name='files')

    class Meta:
        db_table = "File"
