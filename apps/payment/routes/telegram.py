from rest_framework.generics import CreateAPIView

from apps.payment.models import Payment
from apps.payment.serializers.telegram import CustomerLoadPaymentSerializer, CustomerDeliverySerializer
from apps.tools.models import Delivery
from config.core.permissions.telegram import IsCustomer


class CustomerLoadPayment(CreateAPIView):
    queryset = Payment.objects.select_related('customer')
    serializer_class = CustomerLoadPaymentSerializer
    permission_classes = [IsCustomer, ]


class CustomerDeliveryCreateAPIView(CreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = CustomerDeliverySerializer
    permission_classes = [IsCustomer, ]
