from rest_framework.generics import CreateAPIView

from apps.payment.models import Payment
from apps.payment.serializers.telegram import CustomerLoadPaymentSerializer
from config.core.permissions.telegram import IsCustomer


class CustomerLoadPayment(CreateAPIView):
    queryset = Payment.objects.select_related('customer')
    serializer_class = CustomerLoadPaymentSerializer
    permission_classes = [IsCustomer, ]
