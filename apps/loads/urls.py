from django.urls import path

from apps.loads.views import BarcodeConnectionAPIView

app_name = 'api'
urlpatterns = [
    path('barcode-connection/', BarcodeConnectionAPIView.as_view(), name='barcode_connection')
]
