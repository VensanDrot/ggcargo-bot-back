import json
import locale
from collections import defaultdict
from datetime import timedelta, datetime

from django.conf import settings
from django.utils import timezone
from django.utils.timezone import localdate

from apps.tools.serializer import SettingsSerializer
from apps.tools.tasks import send_newsletter
from apps.user.models import Customer


def division_return_zero(a, b):
    try:
        return ((sum(a) - sum(b)) / sum(b)) * 100
    except ZeroDivisionError:
        return 0


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
    from apps.tools.views import settings_path

    with open(settings_path, 'r') as file:
        file_data = json.load(file)
        settings_serializer = SettingsSerializer(data=file_data)
        settings_serializer.is_valid(raise_exception=True)
        settings_data = settings_serializer.validated_data
        price = settings_data.get('price')
        return price


def dashboard_chart_maker(objects, comparing_objects, start_date, end_date,
                          date_weight_exists=None, date_payment_exists=None):
    date_counts = defaultdict(int)
    date_weight = defaultdict(int) if date_weight_exists else None
    date_payment = defaultdict(int) if date_payment_exists else None
    for obj in objects:
        local_date = localdate(obj.created_at)
        if not date_payment_exists:
            date_counts[local_date] += 1
            if date_weight_exists:
                date_weight[local_date] += obj.weight
        else:
            date_payment[local_date] += obj.paid_amount

    c_date_counts = defaultdict(int)
    c_date_weight = defaultdict(int) if date_weight_exists else None
    c_date_payment = defaultdict(int) if date_payment_exists else None
    for c_obj in comparing_objects:
        c_local_date = localdate(c_obj.created_at)
        if not date_payment_exists:
            c_date_counts[c_local_date] += 1
            if date_weight_exists:
                c_date_weight[c_local_date] += c_obj.weight
        else:
            c_date_payment[c_local_date] += c_obj.paid_amount

    all_dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    for date in all_dates:
        if not date_payment_exists:
            if date not in date_counts:
                date_counts[date] = 0
            if date_weight_exists:
                if date not in date_weight:
                    date_weight[date] = 0
        else:
            if date not in date_payment:
                date_payment[date] = 0

    if not date_payment_exists:
        sorted_dates = sorted(date_counts.keys())
    else:
        sorted_dates = sorted(date_payment.keys())

    locale.setlocale(locale.LC_TIME, settings.SET_LOCAL_LANGUAGE)
    labels = [date.strftime('%b-%d').capitalize() for date in sorted_dates]
    if not date_payment_exists:
        line1 = [date_counts[date] for date in sorted_dates]
        c_line1 = [c_date_counts[date] for date in c_date_counts.keys()]
    else:
        line1 = [date_payment[date] for date in sorted_dates]
        c_line1 = [c_date_payment[date] for date in c_date_payment.keys()]
    chart = {
        'line1': line1,
        # 'line2': line2,
        'labels': labels
    }
    totals_percent = {
        'line1': sum(line1),
        'line1_percent': division_return_zero(line1, c_line1)
    }
    if date_weight:
        line2 = [date_weight[date] for date in sorted_dates]
        c_line2 = [c_date_weight[date] for date in c_date_weight.keys()]
        chart['line2'] = line2
        totals_percent['line2'] = sum(line2)
        totals_percent['line2_percent'] = division_return_zero(line2, c_line2)
    return chart, totals_percent


def generate_non_active_id() -> tuple:
    prefix = 'DELETE'
    customers = Customer.objects.filter(prefix=prefix).order_by('code')
    codes = [int(c.code) for c in customers]
    max_code = max(codes) if codes else 0
    code = str(customers.count() + 1).zfill(4)
    for i in range(1, max_code + 2):
        if i not in codes:
            code = str(i).zfill(4)
            break
    return prefix, code


def create_newsletter_task(newsletter_id, schedule_time):
    schedule_time = schedule_time.replace(tzinfo=None)
    run_time = timezone.make_aware(schedule_time)

    send_newsletter.apply_async(eta=run_time)
