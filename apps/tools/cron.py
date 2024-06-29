import logging

from django.utils import timezone

from apps.tools.utils.helpers import generate_non_active_id
from apps.user.models import Customer

logger = logging.getLogger()


def non_active_customers():
    now = timezone.now()

    customers = Customer.objects.all()
    for customer in customers:
        joined_at = timezone.localtime(customer.user.date_joined)
        joined_days_diff = (now - joined_at).days

        latest_accepted_product = customer.products.order_by('accepted_time_china', 'accepted_time_tashkent').last()
        latest_time = latest_accepted_product.accepted_time_tashkent or latest_accepted_product.accepted_time_china
        latest_product_days_diff = (now - latest_time).days
        if ((joined_days_diff > 90) and (not customer.products.exists())) or (latest_product_days_diff > 90):
            prefix, code = generate_non_active_id()
            ex_prefix, ex_code = customer.prefix, customer.code
            customer.ex_prefix = ex_prefix
            customer.ex_code = ex_code
            customer.prefix = prefix
            customer.code = code
        customer.save()
