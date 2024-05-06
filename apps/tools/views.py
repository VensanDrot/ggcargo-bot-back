from drf_yasg.utils import swagger_auto_schema

from apps.tools.models import PaymentCard, Cost, ChannelLink, WarehouseAddress, SupportService
from apps.tools.serializer import PaymentCardSerializer, CostSerializer, ChannelLinkSerializer, \
    WarehouseAddressSerializer, SupportServiceSerializer
from config.views import ModelViewSetPack


class PaymentCardModelViewSet(ModelViewSetPack):
    queryset = PaymentCard.objects.all()
    serializer_class = PaymentCardSerializer
    post_serializer_class = PaymentCardSerializer

    @swagger_auto_schema(request_body=PaymentCardSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class CostModelViewSet(ModelViewSetPack):
    queryset = Cost.objects.all()
    serializer_class = CostSerializer
    post_serializer_class = CostSerializer

    @swagger_auto_schema(request_body=PaymentCardSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ChannelLinkModelViewSet(ModelViewSetPack):
    queryset = ChannelLink.objects.all()
    serializer_class = ChannelLinkSerializer
    post_serializer_class = ChannelLinkSerializer

    @swagger_auto_schema(request_body=PaymentCardSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class WarehouseAddressModelViewSet(ModelViewSetPack):
    queryset = WarehouseAddress.objects.all()
    serializer_class = WarehouseAddressSerializer
    post_serializer_class = WarehouseAddressSerializer

    @swagger_auto_schema(request_body=PaymentCardSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class SupportServiceModelViewSet(ModelViewSetPack):
    queryset = SupportService.objects.all()
    serializer_class = SupportServiceSerializer
    post_serializer_class = SupportServiceSerializer

    @swagger_auto_schema(request_body=PaymentCardSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
