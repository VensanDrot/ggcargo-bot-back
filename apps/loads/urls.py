from django.urls import path

from apps.loads.routes.telegram import BarcodeConnectionAPIView, AcceptProductAPIView, OperatorStatisticsAPIView, \
    CustomerProductsListAPIView, AddLoadAPIView, LoadCostAPIView
from apps.loads.routes.web import AdminProductListAPIView, AdminSelectProductStatus, AdminAddProduct, \
    AdminUpdateProduct, AdminDeleteProduct

app_name = 'api'

urlpatterns = [
    # admin
    path('admin/delivery/products/', AdminProductListAPIView.as_view(), name='admin_delivery_products'),
    path('admin/delivery/product-statuses/', AdminSelectProductStatus.as_view(), name='admin_select_status'),
    path('admin/delivery/product-add/', AdminAddProduct.as_view(), name='admin_add_product'),
    path('admin/delivery/product-update/<int:pk>/', AdminUpdateProduct.as_view(), name='admin_update_product'),
    path('admin/delivery/product-delete/<int:pk>/', AdminDeleteProduct.as_view(), name='admin_delete_product'),

    # bot
    path('operator/china/barcode-connection/', BarcodeConnectionAPIView.as_view(), name='china_barcode'),
    path('operator/tashkent/accept-product/<str:barcode>/', AcceptProductAPIView.as_view(), name='tashkent_accept'),
    path('operator/daily-stats/', OperatorStatisticsAPIView.as_view(), name='operator_daily_stats'),
    path('operator/tashkent/<str:customer_id>/products/', CustomerProductsListAPIView.as_view(),
         name='tashkent_customers_product_list'),
    path('operator/tashkent/add-load/', AddLoadAPIView.as_view(), name='tashkent_add_load'),
    path('operator/tashkent/load-cost/', LoadCostAPIView.as_view(), name='tashkent_load_cost'),

    # common
]
