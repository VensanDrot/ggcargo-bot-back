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

        latest_accepted_product = timezone.localtime(customer.products.latest('accepted_time_china').accepted_time_china)
        if (((joined_days_diff > 90) and (not customer.products.exists()))
                or (now_expires_at < customer.products.latest('accepted_time_china').accepted_time_china)):
            prefix, code = generate_non_active_id()
            customer.prefix = prefix
            customer.code = code
        customer.save()
