from django.urls import path

from apps.loads.views import BarcodeConnectionAPIView, AcceptProductAPIView, OperatorStatisticsAPIView, \
    CustomerProductsListAPIView, AddLoadAPIView

app_name = 'api'
urlpatterns = [
    path('operator/china/barcode-connection/', BarcodeConnectionAPIView.as_view(), name='china_barcode'),
    path('operator/tashkent/accept-product/<str:barcode>/', AcceptProductAPIView.as_view(), name='tashkent_accept'),
    path('operator/stats/', OperatorStatisticsAPIView.as_view(), name='operator_stats'),
    path('operator/tashkent/<str:customer_id>/products/', CustomerProductsListAPIView.as_view(),
         name='tashkent_customers_product_list'),
    path('operator/tashkent/add-load/', AddLoadAPIView.as_view(), name='tashkent_add_load'),
]

