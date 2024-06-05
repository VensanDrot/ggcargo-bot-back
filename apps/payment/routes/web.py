from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter

from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payment.filter import AdminPaymentFilter, PaymentSearchFilter
from apps.payment.models import Payment
from apps.payment.serializers.web import AdminPaymentOpenListSerializer, AdminPaymentClosedListSerializer, \
    AdminPaymentDeclineSerializer, AdminPaymentApplySerializer
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
    serializer_class = AdminPaymentApplySerializer

    @swagger_auto_schema(request_body=AdminPaymentApplySerializer)
    def patch(self, request, payment_id, *args, **kwargs):
        instance = get_object_or_404(Payment, pk=payment_id)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
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
        instance.status = 'SUCCESSFUL'
        instance.operator_id = request.user.id
        instance.save()
        return Response({
            'id': instance.id,
            'customer_id': f'{instance.customer.prefix}{instance.customer.code}',
            'paid_amount': instance.paid_amount,
            'comment': instance.comment,
            'status': instance.status,
            'status_display': instance.get_status_display(),
            'image': instance.files.values('name', 'size', 'path'),
        })


class AdminPaymentDeclineAPIView(APIView):
    serializer_class = AdminPaymentDeclineSerializer

    @swagger_auto_schema(request_body=AdminPaymentDeclineSerializer)
    def patch(self, request, payment_id, *args, **kwargs):
        instance = get_object_or_404(Payment, pk=payment_id)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance.status = 'DECLINED'
        instance.operator_id = request.user.id
        instance.save()
        return Response({
            'id': instance.id,
            'customer_id': f'{instance.customer.prefix}{instance.customer.code}',
            'paid_amount': instance.paid_amount,
            'comment': instance.comment,
            'status': instance.status,
            'status_display': instance.get_status_display(),
            'image': instance.files.values('name', 'size', 'path'),
        })
