from rest_framework import permissions

from apps.user.models import User


class LandingPage(permissions.BasePermission):
    """
    Allow users to GET requests
    """

    def has_permission(self, request, view):
        if view.action == 'list' or view.action == 'retrieve':
            return True
        return request.user.is_authenticated


class IsOperator(permissions.BasePermission):
    """
    Allow if user has operator relation
    """

    def has_permission(self, request, view):
        user: User = request.user
        if user.is_authenticated:
            if hasattr(user, 'operator'):
                return True
        return False
