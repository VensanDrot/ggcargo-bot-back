from django.db.models import Q
from django_filters import FilterSet, DateFilter
from rest_framework.filters import BaseFilterBackend

from apps.loads.models import Product, Load
from apps.tools.utils.helpers import split_code


class AdminProductFilter(FilterSet):
    date = DateFilter(method='filter_date')

    @staticmethod
    def filter_date(queryset, name, value):
        return queryset.filter(updated_at__date=value)

    class Meta:
        model = Product
        fields = ['status',
                  'date', ]


class AdminLoadFilter(FilterSet):
    date = DateFilter(method='filter_date')

    @staticmethod
    def filter_date(queryset, name, value):
        return queryset.filter(updated_at__date=value)

    class Meta:
        model = Load
        fields = ['status',
                  'date', ]


class ProductSearchFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', '')
        if search_param:
            prefix, code = split_code(search_param)
            queryset = queryset.filter(
                Q(barcode__icontains=search_param) |
                Q(accepted_by_china__full_name__icontains=search_param) |
                Q(
                    Q(customer__prefix__icontains=prefix) &
                    Q(customer__code__icontains=code)
                )
            )
        return queryset


class LoadSearchFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', '')
        if search_param:
            prefix, code = split_code(search_param)
            queryset = queryset.filter(
                Q(weight__icontains=search_param) |
                Q(cost__icontains=search_param) |
                Q(
                    Q(customer__prefix__icontains=prefix) &
                    Q(customer__code__icontains=code)
                )
            )
        return queryset
