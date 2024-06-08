from django.urls import path

from apps.integrations.views import EMUAuthAPIView

urlpatterns = [
    path('emu/auth/', EMUAuthAPIView.as_view(), name='emu_auth'),
]
