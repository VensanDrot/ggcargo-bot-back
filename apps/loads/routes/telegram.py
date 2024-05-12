from datetime import datetime

from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.loads.models import Product, Load
from apps.loads.serializers.telegram import BarcodeConnectionSerializer, AcceptProductSerializer, ProductListSerializer, \
    AddLoadSerializer
from apps.tools.utils.helpers import accepted_today
from apps.user.models import User
from config.core.api_exceptions import APIValidation
from config.core.permissions.telegram import IsTashkentTGOperator, IsChinaTGOperator, IsTGOperator


class OperatorStatisticsAPIView(APIView):
    queryset = User.objects.filter(operator__isnull=False)
    permission_classes = [IsTGOperator, ]

    @staticmethod
    def get(request, *args, **kwargs):
        user = request.user
        return Response({"accepted_today": accepted_today(user)})


class BarcodeConnectionAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = BarcodeConnectionSerializer
    permission_classes = [IsChinaTGOperator, ]


class AcceptProductAPIView(APIView):
    queryset = Product.objects.all()
    serializer_class = AcceptProductSerializer
    permission_classes = [IsTashkentTGOperator, ]

    def get_object(self):
        try:
            return Product.objects.get(barcode=self.kwargs['barcode'])
        except Product.DoesNotExist:
            raise APIValidation("Product does not exist or barcode was not provided",
                                status_code=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AcceptProductSerializer)
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance.status = 'DELIVERED'
        instance.accepted_by_tashkent = request.user
        instance.accepted_time_tashkent = datetime.now()
        instance.save()
        return Response({'detail': 'Product accepted'})


class CustomerProductsListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsTashkentTGOperator, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('customer_id'):
            queryset = queryset.filter(
                Q(customer__prefix=self.kwargs['customer_id'][:3]) & Q(customer__code=self.kwargs['customer_id'][3:])
            )
        return queryset


class AddLoadAPIView(CreateAPIView):
    queryset = Load.objects.all()
    serializer_class = AddLoadSerializer
