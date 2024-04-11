from rest_framework.generics import CreateAPIView

from apps.loads.models import Product
from apps.loads.serializer import BarcodeConnectionSerializer


class BarcodeConnectionAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = BarcodeConnectionSerializer

