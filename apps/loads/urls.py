from django.urls import path

from apps.loads.views import BarcodeConnectionAPIView, AcceptProductAPIView, OperatorStatisticsAPIView

app_name = 'api'
urlpatterns = [
    path('barcode-connection/', BarcodeConnectionAPIView.as_view(), name='barcode_connection'),
    path('accept-product/<str:barcode>/', AcceptProductAPIView.as_view(), name='accept_product'),
    path('operator/stats/', OperatorStatisticsAPIView.as_view(), name='operator_china_stats'),
]
