from rest_framework import permissions

from apps.user.models import User


class IsTGOperator(permissions.BasePermission):
    """
    Allow if user has telegram operator relation
    """

    def has_permission(self, request, view):
        user: User = request.user
        if user.is_superuser:
            return True
        if user.is_authenticated:
            if hasattr(user, 'operator'):
                if user.operator.operator_type == 'TELEGRAM':
                    return True
        return False


class IsTGAdminOperator(permissions.BasePermission):
    """
    Allow if user has telegram operator relation, if is_admin field is True
    """

    def has_permission(self, request, view):
        user: User = request.user
        if user.is_superuser:
            return True
        if user.is_authenticated:
            if hasattr(user, 'operator'):
                if not user.operator.operator_type == 'TELEGRAM':
                    return False
                is_admin = user.operator.is_admin
                if is_admin:
                    return True
                return False
        return False


class IsTashkentTGOperator(permissions.BasePermission):
    """
    Allow if user is telegram Tashkent Operator
    """

    def has_permission(self, request, view):
        user: User = request.user
        if user.is_superuser:
            return True
        if user.is_authenticated:
            if hasattr(user, 'operator'):
                if not user.operator.operator_type == 'TELEGRAM':
                    return False
                warehouse = user.operator.warehouse
                if warehouse == 'TASHKENT':
                    return True
        return False


class IsChinaTGOperator(permissions.BasePermission):
    """
    Allow if user is China telegram Operator
    """

    def has_permission(self, request, view):
        user: User = request.user
        if user.is_superuser:
            return True
        if user.is_authenticated:
            if hasattr(user, 'operator'):
                if not user.operator.operator_type == 'TELEGRAM':
                    return False
                warehouse = user.operator.warehouse
                if warehouse == 'CHINA':
                    return True
        return False
