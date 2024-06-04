from django_filters import FilterSet, ChoiceFilter

from apps.user.models import User
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
