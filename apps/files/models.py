from django.db import models

from config.models import BaseModel


class File(BaseModel):
    name = models.CharField(max_length=300, null=True)
    gen_name = models.CharField(max_length=100, null=True)
    size = models.FloatField(null=True)
    path = models.TextField(null=True)
    content_type = models.CharField(max_length=100, null=True)
    extension = models.CharField(max_length=30, null=True)
    product = models.ForeignKey("tools.Product", on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='files')
    loads = models.ForeignKey("loads.Load", on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='files')

    class Meta:
        db_table = "File"
