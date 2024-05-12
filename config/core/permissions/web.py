from rest_framework import permissions

from apps.user.models import User


class IsWebOperator(permissions.BasePermission):
    """
    Allow if user has web operator relation
    """

    def has_permission(self, request, view):
        user: User = request.user
        if user.is_superuser:
            return True
        if user.is_authenticated:
            if hasattr(user, 'operator'):
                if user.operator.operator_type == 'WEB':
                    return True
        return False
