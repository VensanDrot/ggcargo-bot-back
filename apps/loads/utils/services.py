from django.utils.timezone import localdate
from rest_framework.generics import get_object_or_404

from apps.payment.models import Payment
from config.core.api_exceptions import APIValidation


def process_payment(request, serializer_class, application_id, payment_status):
    try:
        instance = get_object_or_404(Payment, pk=application_id)
        serializer = serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance: Payment = serializer.save()
        data = serializer.data
        instance.status = payment_status
        if payment_status == 'SUCCESSFUL':
            instance.customer.debt = min(instance.customer.debt - data.get('paid_amount', 0), 0)
            instance.customer.save()
            if instance.customer.debt == 0:
                instance.load.status = 'PAID'
                instance.load.save()
            elif instance.customer.debt == instance.load.cost:
                instance.load.status = 'NOT_PAID'
                instance.load.save()
            elif instance.customer.debt != instance.load.customer:
                instance.load.status = 'PARTIALLY_PAID'
                instance.load.save()
        instance.operator_id = request.user.id
        instance.save()
        return {
            'id': instance.id,
            'customer_id': f'{instance.customer.prefix}{instance.customer.code}',
            'paid_amount': data.get('paid_amount'),
            'debt': instance.customer.debt,
            'date': localdate(instance.updated_at),
            'comment': data.get('comment'),
            'status': instance.status,
            'status_display': instance.get_status_display(),
        }
    except Exception as exc:
        raise APIValidation(f'Error occurred: {exc.args}')
