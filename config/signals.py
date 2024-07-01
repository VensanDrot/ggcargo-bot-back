from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.tools.tasks import send_newsletter

from apps.tools.models import Newsletter


@receiver(post_save, sender=Newsletter)
def schedule_newsletter_task(sender, instance, **kwargs):
    if instance.send_date and instance.send_date > timezone.now():
        send_newsletter.apply_async((instance.id,), eta=instance.send_date)
