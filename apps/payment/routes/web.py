from django.utils.timezone import localdate
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.filter import AdminPaymentFilter, PaymentSearchFilter
from apps.payment.models import Payment
from apps.payment.serializers.web import AdminPaymentOpenListSerializer, AdminPaymentClosedListSerializer, \
    AdminPaymentDeclineSerializer, AdminPaymentApplySerializer
from config.core.api_exceptions import APIValidation
from config.core.pagination import APIPagination
from config.core.permissions.web import IsWebOperator


class AdminPaymentOpenListAPIView(ListAPIView):
    queryset = Payment.objects.filter(status__isnull=True)
    serializer_class = AdminPaymentOpenListSerializer
    permission_classes = [IsWebOperator, ]
    pagination_class = APIPagination
    filter_backends = [DjangoFilterBackend, PaymentSearchFilter, ]
    search_fields = ['customer__prefix', 'customer__code', ]


class AdminPaymentClosedListAPIView(ListAPIView):
    queryset = Payment.objects.filter(status__isnull=False)
    serializer_class = AdminPaymentClosedListSerializer
    permission_classes = [IsWebOperator, ]
    pagination_class = APIPagination
    filterset_class = AdminPaymentFilter
    filter_backends = [DjangoFilterBackend, PaymentSearchFilter, ]
    search_fields = ['customer__prefix', 'customer__code', 'paid_amount']


class AdminPaymentApplyAPIView(APIView):
    # serializer_class = AdminPaymentApplySerializer
    permission_classes = [IsWebOperator, ]

    # @swagger_auto_schema(request_body=AdminPaymentApplySerializer)
    def patch(self, request, payment_id, *args, **kwargs):
        instance = get_object_or_404(Payment, pk=payment_id)
        instance.customer.debt = 0
        instance.load.status = 'PAID'
        instance.status = 'SUCCESSFUL'
        instance.operator_id = request.user.id
        instance.customer.save()
        instance.load.save()
        instance.save()
        return Response({
            'id': instance.id,
            'customer_id': f'{instance.customer.prefix}{instance.customer.code}',
            'date': localdate(instance.created_at),
            'files': instance.files.values('name', 'size', 'path'),
            'status': instance.status,
            'status_display': instance.get_status_display(),
            'debt': instance.customer.debt,
            'paid_amount': instance.paid_amount,
            'comment': instance.comment,
        })


class AdminPaymentDeclineAPIView(APIView):
    serializer_class = AdminPaymentDeclineSerializer
    permission_classes = [IsWebOperator, ]

    @swagger_auto_schema(request_body=AdminPaymentDeclineSerializer)
    def patch(self, request, payment_id, *args, **kwargs):
        instance = get_object_or_404(Payment, pk=payment_id)
        if instance.customer.debt < request.data.get('paid_amount'):
            raise APIValidation(_('Выплаченная сумма больше долга клиента'), status_code=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        instance.customer.debt = instance.customer.debt - data.get('paid_amount', 0)
        instance.customer.save()
        if instance.customer.debt == 0:
            instance.load.status = 'PAID'
            instance.load.save()
        elif instance.customer.debt == instance.load.cost:
            instance.load.status = 'NOT_PAID'
            instance.load.save()
        elif instance.customer.debt != instance.load.cost:
            instance.load.status = 'PARTIALLY_PAID'
            instance.load.save()
        instance.status = 'DECLINED'
        instance.operator_id = request.user.id
        instance.save()
        return Response({
            'id': instance.id,
            'customer_id': f'{instance.customer.prefix}{instance.customer.code}',
            'date': localdate(instance.created_at),
            'files': instance.files.values('name', 'size', 'path'),
            'status': instance.status,
            'status_display': instance.get_status_display(),
            'debt': instance.customer.debt,
            'paid_amount': instance.paid_amount,
            'comment': instance.comment,
        })
