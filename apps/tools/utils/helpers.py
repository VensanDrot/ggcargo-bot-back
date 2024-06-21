import json
import pytz

from datetime import datetime

from django.utils import timezone
from django.utils.timezone import localtime
from django.db.models import Sum

from apps.tools.serializer import SettingsSerializer
from apps.tools.views import settings_path


def split_code(full_code):
    prefix = ""
    code = ""

    for char in full_code:
        if char.isdigit():
            code += char
        else:
            prefix += char
    return prefix, code


def products_accepted_today(user):
    if user.operator.warehouse == 'CHINA':
        count = user.products_china.filter(accepted_time_china__date=timezone.now().date()).count()
    else:
        count = user.products_tashkent.filter(accepted_time_tashkent__date=timezone.now().date()).count()
    return count


def loads_accepted_today(user):
    count = (
        user.load_accepted
        .filter(accepted_time__date=timezone.now().date())
        .count()
    )
    return count if count else 0


def get_price():
    with open(settings_path, 'r') as file:
        file_data = json.load(file)
        settings_serializer = SettingsSerializer(data=file_data)
        settings_serializer.is_valid(raise_exception=True)
        settings_data = settings_serializer.validated_data
        price = settings_data.get('price')
        return price
