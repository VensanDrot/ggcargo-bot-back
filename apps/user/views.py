from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.models import User
from apps.user.serializer import PostUserSerializer, GetUserSerializer, JWTLoginSerializer, PostCustomerSerializer, \
    GetCustomerSerializer
from config.core.pagination import APIPagination
from config.views import ModelViewSetPack


class JWTObtainPairView(TokenObtainPairView):
    serializer_class = JWTLoginSerializer
    permission_classes = [AllowAny, ]


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


class CustomerModelViewSet(ModelViewSetPack):
    queryset = User.objects.filter(customers__isnull=False)
    # serializer_class = GetCustomerSerializer
    # post_serializer_class = PostCustomerSerializer
    pagination_class = APIPagination
#
#     @swagger_auto_schema(request_body=PostCustomerSerializer)
#     def update(self, request, *args, **kwargs):
#         return super().update(request, *args, **kwargs)
#
#     @swagger_auto_schema(request_body=PostCustomerSerializer)
#     def partial_update(self, request, *args, **kwargs):
#         return super().partial_update(request, *args, **kwargs)
