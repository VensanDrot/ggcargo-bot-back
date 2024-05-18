from django.urls import path

from apps.payment.routes.telegram import CustomerLoadPayment

app_name = 'payment'
urlpatterns = [
    path('customer/load-payment/', CustomerLoadPayment.as_view(), name='customer_load_payment'),
]
