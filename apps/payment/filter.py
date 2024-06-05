from django.db.models import Q
from django_filters import FilterSet
from rest_framework.filters import SearchFilter

from apps.payment.models import Payment
from apps.tools.utils.helpers import split_code


class AdminPaymentFilter(FilterSet):
    class Meta:
        model = Payment
        fields = ['status', ]


class PaymentSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', '')
        if search_param:
            prefix, code = split_code(search_param)
            queryset = queryset.filter(
                Q(paid_amount__icontains=search_param) |
                Q(
                    Q(customer__prefix__icontains=prefix) & Q(customer__code__icontains=code)
                )
            )
        return queryset
