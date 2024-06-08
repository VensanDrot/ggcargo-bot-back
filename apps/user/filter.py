from django.db.models import Q
from django_filters import FilterSet, ChoiceFilter
from rest_framework.filters import SearchFilter

from apps.tools.utils.helpers import split_code
from apps.user.models import User, CustomerRegistration
from config.core.choices import WEB_OR_TELEGRAM_CHOICE, WAREHOUSE_CHOICE


class UserStaffFilter(FilterSet):
    operator_type = ChoiceFilter(method='filter_operator_type', choices=WEB_OR_TELEGRAM_CHOICE)
    warehouse = ChoiceFilter(method='filter_warehouse', choices=WAREHOUSE_CHOICE)

    @staticmethod
    def filter_operator_type(queryset, name, value):
        return queryset.filter(operator__operator_type=value)

    @staticmethod
    def filter_warehouse(queryset, name, value):
        return queryset.filter(operator__warehouse=value)

    class Meta:
        model = User
        fields = ['operator_type',
                  'warehouse', ]


class CustomerModerationFilter(FilterSet):
    class Meta:
        model = CustomerRegistration
        fields = ['status']


class CustomerSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', '')
        if search_param:
            prefix, code = split_code(search_param)
            queryset = queryset.filter(
                Q(customer__phone_number__icontains=search_param) |
                Q(full_name__icontains=search_param) |
                Q(
                    Q(customer__prefix__icontains=prefix) &
                    Q(customer__code__icontains=code)
                )
            )
        return queryset


class CustomerModerationSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', '')
        if search_param:
            prefix, code = split_code(search_param)
            queryset = queryset.filter(
                Q(customer__user_type__icontains=search_param) |
                Q(customer__phone_number__icontains=search_param) |
                Q(customer__debt__icontains=search_param) |
                Q(customer__user__full_name__icontains=search_param) |
                Q(customer__accepted_by__full_name__icontains=search_param) |
                Q(
                    Q(customer__prefix__icontains=prefix) &
                    Q(customer__code__icontains=code)
                )
            )
        return queryset
