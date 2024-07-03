from django.urls import path

from apps.integrations.views import EMUAuthAPIView, RegionEMUListAPIView, DistrictEMUListAPIView, OrderEMUAPIView, \
    EMUTrackingAPIView

urlpatterns = [
    path('emu/auth/', EMUAuthAPIView.as_view(), name='emu_auth'),
    # path('emu/regions/', RegionEMUListAPIView.as_view(), name='emu_regions'),
    # path('emu/districts/<str:region>/', DistrictEMUListAPIView.as_view(), name='emu_districts'),
    path('emu/order/', OrderEMUAPIView.as_view(), name='emu_order'),
    path('emu/track/', EMUTrackingAPIView.as_view(), name='emu_track'),
]
