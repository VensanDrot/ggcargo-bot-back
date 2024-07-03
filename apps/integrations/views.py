from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.integrations.emu.data import emu_auth, emu_order, emu_tracking_link
from apps.integrations.models import RegionEMU
from apps.integrations.serializer import DistrictEMUSerializer, OrderEMUSerializer


class EMUAuthAPIView(APIView):
    def get(self, request, *args, **kwargs):
        response = emu_auth()
        response = response.text
        return Response(response)


class RegionEMUListAPIView(APIView):
    queryset = RegionEMU.objects.only('region').values_list()

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        response = queryset.distinct('region').values_list('region', flat=True)
        return Response(response)


class DistrictEMUListAPIView(ListAPIView):
    queryset = RegionEMU.objects.all()
    serializer_class = DistrictEMUSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(region=self.kwargs['region'])
        return queryset


class OrderEMUAPIView(APIView):
    serializer_class = OrderEMUSerializer

    @swagger_auto_schema(request_body=OrderEMUSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data
        # data['customer'] = request.user.customer.id
        order_serializer = self.serializer_class(data=data)
        order_serializer.is_valid(raise_exception=True)
        order_instance = order_serializer.save()
        order_response = emu_order(order_id=order_instance.id, customer_full_name=request.user.full_name,
                                   order_instance=order_instance)
        return Response(order_response.text)


class EMUTrackingAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[
        Parameter('order_number', IN_QUERY, description="Order number", type=TYPE_STRING, required=True),
    ])
    def get(self, request, *args, **kwargs):
        order_number = request.query_params.get('order_number')
        response = emu_tracking_link(order_number)
        return Response(response)
