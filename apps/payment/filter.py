from django_filters import FilterSet

from apps.payment.models import Payment


class AdminPaymentFilter(FilterSet):
    class Meta:
        model = Payment
        fields = ['status', ]
