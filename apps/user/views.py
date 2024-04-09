from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.models import User
from apps.user.serializer import PostUserSerializer, GetUserSerializer, AdminLoginSerializer, CustomerLoginSerializer
from config.core.pagination import APIPagination
from config.views import ModelViewSetPack


class AdminJWTObtainPairView(TokenObtainPairView):
    serializer_class = AdminLoginSerializer
    permission_classes = [AllowAny, ]


class CustomerJWTObtainPairView(TokenObtainPairView):
    serializer_class = CustomerLoginSerializer
    permission_classes = [AllowAny, ]


# TODO: end this view, double auth (for customers and admins)

class UserModelViewSet(ModelViewSetPack):
    queryset = User.objects.filter(operators__isnull=False)
    serializer_class = GetUserSerializer
    post_serializer_class = PostUserSerializer
    pagination_class = APIPagination

    @swagger_auto_schema(request_body=PostUserSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=PostUserSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
