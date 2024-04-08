from django.urls import path

from apps.user.views import UserCreateAPIView

app_name = 'staff'
urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
]
