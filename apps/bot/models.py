from django.db import models

from config.core.choices import CAR_OR_AIR_CHOICE


class StartedTG(models.Model):
    tg_id = models.BigIntegerField()
    bot_type = models.CharField(choices=CAR_OR_AIR_CHOICE, max_length=4)

    class Meta:
        db_table = 'StartedTG'
