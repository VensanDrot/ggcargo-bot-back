from celery import shared_task
from rest_framework.generics import get_object_or_404

from apps.bot.views import avia_customer_bot, auto_customer_bot
from apps.tools.models import Newsletter
from apps.user.models import Customer


# @shared_task
def send_newsletter(newsletter_id):
    try:
        newsletter = get_object_or_404(Newsletter, pk=newsletter_id)
        message = newsletter.text_uz if newsletter.text_uz else newsletter.text_ru
        photo_path = newsletter.photo_uz.path if newsletter.photo_uz else newsletter.photo_ru.path
        photo_url = f'https://backend.gogocargo.uz/{photo_path}'
        customers = Customer.objects.select_related('passport_photo', 'accepted_by', 'user')

        if newsletter.bot_type == 'AVIA':
            for customer in customers.filter(user_type='AVIA'):
                avia_customer_bot.send_photo(customer.tg_id, photo_url, message)
        elif newsletter.bot_type == 'AUTO':
            for customer in customers.filter(user_type='AUTO'):
                auto_customer_bot.send_message(customer.tg_id, photo_url, message)

        newsletter.status = 'SENT'
        newsletter.save()
    except Newsletter.DoesNotExist:
        pass
