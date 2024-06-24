from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.loads.models import Product
from apps.loads.serializers.general import OpenProductBarcodeSerializer


class OpenProductBarcodeAPIView(RetrieveAPIView):
    queryset = Product.objects.select_related('customer', 'accepted_by_china', 'accepted_by_tashkent')
    serializer_class = OpenProductBarcodeSerializer
    permission_classes = [AllowAny, ]
    lookup_field = 'barcode'
