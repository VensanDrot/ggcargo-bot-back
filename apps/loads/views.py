import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.loads.serializers.general import LoadCostSerializer
from apps.tools.serializer import SettingsSerializer
from apps.tools.views import settings_path


class LoadCostAPIView(APIView):
    serializer_class = LoadCostSerializer

    @swagger_auto_schema(request_body=LoadCostSerializer)
    def post(self, request, *args, **kwargs):
        with open(settings_path, 'r') as file:
            file_data = json.load(file)
            settings_serializer = SettingsSerializer(data=file_data)
            settings_serializer.is_valid(raise_exception=True)
            settings_data = settings_serializer.validated_data
            price = settings_data.get('price')

            cost_serializer = self.serializer_class(data=request.data)
            cost_serializer.is_valid(raise_exception=True)
            response = cost_serializer.calculate_cost(price)
        return Response({'load_cost': response})
