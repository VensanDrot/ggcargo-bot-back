from rest_framework.generics import CreateAPIView

from apps.user.models import User
from apps.user.serializer import UserCreateSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
