from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.loads.filter import AdminProductFilter, AdminLoadFilter, ProductSearchFilter, LoadSearchFilter
from apps.loads.models import Product, Load
from apps.loads.serializers.web import AdminProductListSerializer, AdminAddProductSerializer, AdminLoadListSerializer, \
    AdminLoadRetrieveSerializer, AdminLoadUpdateSerializer
from config.core.choices import PRODUCT_STATUS_CHOICE
from config.core.pagination import APIPagination
from config.core.permissions.web import IsWebOperator


class AdminProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = AdminProductListSerializer
    permission_classes = [IsWebOperator, ]
    pagination_class = APIPagination
    filterset_class = AdminProductFilter
    filter_backends = [DjangoFilterBackend, ProductSearchFilter, ]
    search_fields = ['barcode', 'customer__prefix', 'customer__code', 'accepted_by_china__full_name', ]


class AdminSelectProductStatus(APIView):
    permission_classes = [IsWebOperator, ]

    @staticmethod
    def get(request, *args, **kwargs):
        response = []
        for product_status in PRODUCT_STATUS_CHOICE:
            if product_status[0] == 'NOT_LOADED':
                continue
            response.append({
                'value': product_status[0],
                'label': product_status[1],
            })
        return Response(response)


class AdminAddProduct(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = AdminAddProductSerializer
    permission_classes = [IsWebOperator, ]


class AdminUpdateProduct(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = AdminAddProductSerializer
    permission_classes = [IsWebOperator, ]
    http_method_names = ['patch', ]


class AdminDeleteProduct(DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsWebOperator, ]


class AdminLoadListAPIView(ListAPIView):
    queryset = Load.objects.select_related('customer', 'accepted_by').prefetch_related('products')
    serializer_class = AdminLoadListSerializer
    permission_classes = [IsWebOperator, ]
    filterset_class = AdminLoadFilter
    filter_backends = [DjangoFilterBackend, LoadSearchFilter, ]
    search_fields = ['weight', 'customer__prefix', 'customer__code', 'cost']
    pagination_class = APIPagination


class AdminLoadRetrieveAPIView(RetrieveAPIView):
    queryset = Load.objects.select_related('customer', 'accepted_by').prefetch_related('products')
    serializer_class = AdminLoadRetrieveSerializer
    permission_classes = [IsWebOperator, ]


class AdminLoadUpdateAPIView(UpdateAPIView):
    queryset = Load.objects.select_related('customer', 'accepted_by').prefetch_related('products')
    serializer_class = AdminLoadUpdateSerializer
    permission_classes = [IsWebOperator, ]
    http_method_names = ['patch']
