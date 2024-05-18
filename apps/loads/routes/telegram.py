from datetime import datetime

from django.db.models import Q
from django.utils.timezone import localdate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.loads.models import Product, Load
from apps.loads.serializers.telegram import BarcodeConnectionSerializer, LoadInfoSerializer, AddLoadSerializer, \
    ModerationNotProcessedLoadSerializer, CustomerCurrentLoadSerializer, CustomerOwnLoadsSerializer, \
    ModerationProcessedLoadSerializer, ModerationLoadPaymentSerializer, ModerationLoadApplySerializer, \
    ModerationLoadDeclineSerializer
from apps.payment.models import Payment
from apps.tools.utils.helpers import products_accepted_today, get_price, loads_accepted_today
from apps.user.models import User
from config.core.api_exceptions import APIValidation
from config.core.permissions.telegram import IsTashkentTGOperator, IsChinaTGOperator, IsTGOperator, IsCustomer


class OperatorStatisticsAPIView(APIView):
    queryset = User.objects.filter(operator__isnull=False)
    permission_classes = [IsTGOperator, ]

    @staticmethod
    def get(request, *args, **kwargs):
        user = request.user
        if user.operator.warehouse == 'CHINA':
            response = {'products': products_accepted_today(user)}
        else:
            response = {
                'products': products_accepted_today(user),
                'loads': loads_accepted_today(user)
            }
        return Response(response)


class BarcodeConnectionAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = BarcodeConnectionSerializer
    permission_classes = [IsChinaTGOperator, ]


class AcceptProductAPIView(APIView):
    queryset = Product.objects.all()
    permission_classes = [IsTashkentTGOperator, ]

    def get_object(self):
        try:
            return Product.objects.get(barcode=self.kwargs['barcode'])
        except Product.DoesNotExist:
            raise APIValidation("Product does not exist or barcode was not provided",
                                status_code=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'DELIVERED'
        instance.accepted_by_tashkent = request.user
        instance.accepted_time_tashkent = datetime.now()
        instance.save()
        return Response({'detail': 'Product accepted'})


class LoadInfoAPIView(APIView):
    queryset = Product.objects.all()
    serializer_class = LoadInfoSerializer
    permission_classes = [IsTashkentTGOperator, ]

    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs.get('customer_id'):
            queryset = queryset.filter((Q(customer__prefix=self.kwargs['customer_id'][:3]) &
                                        Q(customer__code=self.kwargs['customer_id'][3:])) & Q(status='DELIVERED'))
        return queryset

    @swagger_auto_schema(request_body=LoadInfoSerializer)
    def post(self, request, *args, **kwargs):
        price = get_price()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.response(price)
        return Response(response)


class AddLoadAPIView(CreateAPIView):
    queryset = Load.objects.all()
    serializer_class = AddLoadSerializer
    permission_classes = [IsTashkentTGOperator, ]


class ReleaseLoadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        return


class ModerationNotProcessedLoadAPIView(ListAPIView):
    queryset = Payment.objects.select_related('customer', 'load').filter(status__isnull=True)
    serializer_class = ModerationNotProcessedLoadSerializer
    permission_classes = [IsTashkentTGOperator, ]


class ModerationProcessedLoadAPIView(ListAPIView):
    queryset = Payment.objects.select_related('customer', 'load').filter(status__isnull=False)
    serializer_class = ModerationProcessedLoadSerializer
    permission_classes = [IsTashkentTGOperator, ]


class ModerationLoadPaymentAPIView(APIView):
    serializer_class = ModerationLoadPaymentSerializer

    def get(self, request, application_id, *args, **kwargs):
        instance = get_object_or_404(Payment, pk=application_id)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


def process_payment(request, serializer_class, application_id, payment_status):
    try:
        instance = get_object_or_404(Payment, pk=application_id)
        serializer = serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance: Payment = serializer.save()
        data = serializer.data
        instance.status = payment_status
        if payment_status == 'SUCCESSFUL':
            instance.customer.debt -= data.get('paid_amount', 0)
            instance.customer.save()
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


class ModerationLoadApplyAPIView(APIView):
    serializer_class = ModerationLoadApplySerializer

    @swagger_auto_schema(request_body=ModerationLoadApplySerializer)
    def post(self, request, application_id, *args, **kwargs):
        response = process_payment(request, ModerationLoadApplySerializer, application_id, 'SUCCESSFUL')
        return Response(response)


class ModerationLoadDeclineAPIView(APIView):
    serializer_class = ModerationLoadDeclineSerializer

    @swagger_auto_schema(request_body=ModerationLoadDeclineSerializer)
    def post(self, request, application_id, *args, **kwargs):
        response = process_payment(request, ModerationLoadDeclineSerializer, application_id, 'DECLINED')
        return Response(response)


# CUSTOMER
class CustomerCurrentLoadAPIView(APIView):
    queryset = (Load.objects
                .select_related('customer', 'accepted_by')
                .prefetch_related('products')
                .filter(status='CREATED'))
    serializer_class = CustomerCurrentLoadSerializer
    permission_classes = [IsCustomer, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        instance = self.queryset.filter(customer_id=user.customer.id).first()
        serializer = CustomerCurrentLoadSerializer(instance)
        return Response(serializer.data)


class CustomerOwnLoadsHistoryAPIView(ListAPIView):
    queryset = Load.objects.select_related('customer', 'accepted_by').prefetch_related('products').filter(status='DONE')
    serializer_class = CustomerOwnLoadsSerializer
    permission_classes = [IsCustomer, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(customer_id=self.request.user.customer.id)
        return queryset
