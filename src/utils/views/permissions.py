from rest_framework.permissions import (
    AllowAny as AllowAnyPermission,
    IsAuthenticated as IsAuthenticatedPermission,
    IsAdminUser as IsAdminUserPermission,
)
from rest_framework.permissions import BasePermission


class IsAdminSuperUserPermission(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
