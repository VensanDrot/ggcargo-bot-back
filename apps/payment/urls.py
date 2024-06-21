from django.urls import path

from apps.payment.routes.telegram import CustomerLoadPayment, CustomerDeliveryCreateAPIView
from apps.payment.routes.web import AdminPaymentOpenListAPIView, AdminPaymentClosedListAPIView, \
    AdminPaymentApplyAPIView, AdminPaymentDeclineAPIView

app_name = 'payment'
urlpatterns = [
    # admin
    path('admin/opened-list/', AdminPaymentOpenListAPIView.as_view(), name='admin_payment_open_list'),
    path('admin/closed-list/', AdminPaymentClosedListAPIView.as_view(), name='admin_payment_closed_list'),
    path('admin/apply/<int:payment_id>/', AdminPaymentApplyAPIView.as_view(), name='admin_payment_apply'),
    path('admin/decline/<int:payment_id>/', AdminPaymentDeclineAPIView.as_view(), name='admin_payment_decline'),

    # customer-bot
    path('customer/load-payment/', CustomerLoadPayment.as_view(), name='customer_load_payment'),
    path('customer/delivery/', CustomerDeliveryCreateAPIView.as_view(), name='customer_delivery'),
]
