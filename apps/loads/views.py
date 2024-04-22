from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.loads.models import Product
from apps.loads.serializer import BarcodeConnectionSerializer, AcceptProductSerializer
from apps.tools.utils.helpers import accepted_today
from apps.user.models import User
from config.core.api_exceptions import APIValidation
from config.core.permissions import IsTashkentOperator, IsChinaOperator, IsOperator


class OperatorStatisticsAPIView(APIView):
    queryset = User.objects.filter(operator__isnull=False)
    permission_classes = [IsOperator, ]

    @staticmethod
    def get(request, *args, **kwargs):
        user = request.user
        return Response({"accepted_today": accepted_today(user)})


class BarcodeConnectionAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = BarcodeConnectionSerializer
    permission_classes = [IsChinaOperator, ]


class AcceptProductAPIView(APIView):
    queryset = Product.objects.all()
    serializer_class = AcceptProductSerializer
    permission_classes = [IsTashkentOperator, ]

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
