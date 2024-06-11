import xmltodict
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.integrations.emu.data import emu_auth
from apps.integrations.models import RegionEMU
from apps.integrations.serializer import DistrictEMUSerializer


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
