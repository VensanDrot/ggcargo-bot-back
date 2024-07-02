import json
import logging

from celery import shared_task
from rest_framework.generics import get_object_or_404

from apps.bot.views import avia_customer_bot, auto_customer_bot
from apps.tools.models import Newsletter
from apps.user.models import Customer

logger = logging.getLogger()


@shared_task
def send_newsletter(newsletter_id):
    print(newsletter_id)
    logger.debug(f'Task for newsletter: {newsletter_id}')
    # try:
    #     newsletter = get_object_or_404(Newsletter, pk=newsletter_id)
    #     if newsletter.status == 'SENT':
    #         return {'detail': f'Newsletter #{newsletter_id} was sent already', 'status': 400}
    #
    #     message = newsletter.text_uz if newsletter.text_uz else newsletter.text_ru
    #     photo_path = newsletter.photo_uz.path if newsletter.photo_uz else newsletter.photo_ru.path
    #     photo_url = f'https://backend.gogocargo.uz/{photo_path}'
    #     customers = Customer.objects.select_related('passport_photo', 'accepted_by', 'user').filter(tg_id__isnull=False)
    #
    #     if newsletter.bot_type == 'AVIA':
    #         for customer in customers.filter(user_type='AVIA'):
    #             try:
    #                 avia_customer_bot.send_photo(customer.tg_id, photo_url, message)
    #             except Exception as exc:
    #                 continue
    #     elif newsletter.bot_type == 'AUTO':
    #         for customer in customers.filter(user_type='AUTO'):
    #             try:
    #                 auto_customer_bot.send_photo(customer.tg_id, photo_url, message)
    #             except Exception as exc:
    #                 continue
    #
    #     newsletter.status = 'SENT'
    #     newsletter.save()
    #     return {'detail': f'Newsletter #{newsletter_id} sent', 'status': 200}
    # except Newsletter.DoesNotExist:
    #     pass


