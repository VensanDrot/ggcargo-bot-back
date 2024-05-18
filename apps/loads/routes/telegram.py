from datetime import datetime

from django.conf import settings
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.loads.models import Product, Load
from apps.loads.serializers.telegram import BarcodeConnectionSerializer, LoadInfoSerializer, AddLoadSerializer, \
    ModerationNotProcessedLoadSerializer
from apps.tools.utils.helpers import products_accepted_today, get_price, loads_accepted_today
from apps.user.models import User
from config.core.api_exceptions import APIValidation
from config.core.permissions.telegram import IsTashkentTGOperator, IsChinaTGOperator, IsTGOperator


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
        from django.utils.timezone import activate
        activate(settings.TIME_ZONE)
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


class ReleaseLoadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        return


class ModerationNotProcessedLoadAPIView(ListAPIView):
    queryset = Load.objects.select_related('customer', 'accepted_by').prefetch_related('products')
    serializer_class = ModerationNotProcessedLoadSerializer


class ModerationProcessedLoadAPIView(ListAPIView):
    queryset = Load.objects.select_related('customer', 'accepted_by').prefetch_related('products')
