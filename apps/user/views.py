from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.serializer import JWTLoginSerializer, TelegramLoginSerializer
from apps.user.utils.services import authenticate_user, authenticate_telegram_user
from config.core.api_exceptions import APIValidation


class JWTObtainPairView(TokenObtainPairView):
    serializer_class = JWTLoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(authenticate_user(request))
        else:
            raise APIValidation(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class TelegramLoginAPIView(APIView):
    serializer_class = TelegramLoginSerializer
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=TelegramLoginSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            if serializer.validated_data.get('tg_id'):
                return Response(authenticate_telegram_user(request, True))
            else:
                raise APIValidation('tg_id was not provided', status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIValidation(f'Error occurred: {e.args[0]}', status_code=status.HTTP_400_BAD_REQUEST)