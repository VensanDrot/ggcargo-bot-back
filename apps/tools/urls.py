from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.tools.views import SupportServiceModelViewSet, WarehouseAddressModelViewSet, ChannelLinkModelViewSet, \
    CostModelViewSet, PaymentCardModelViewSet

router = DefaultRouter()
router.register(r'payment-card', PaymentCardModelViewSet, basename='payment_card')
router.register(r'cost', CostModelViewSet, basename='cost')
router.register(r'channel-link', ChannelLinkModelViewSet, basename='channel_link')
router.register(r'warehouse-address', WarehouseAddressModelViewSet, basename='warehouse_address')
router.register(r'support-service', SupportServiceModelViewSet, basename='support_service')

app_name = 'tool'
urlpatterns = [
    # path('test/', PaymentCardModelViewSet.as_view({'get': 'list', 'post': 'create'}), name='test')
]
urlpatterns += router.urls
