from django.db.models import Q

from app_user.api.admin.serializers.manage_admin import (
    AdminListAddUpdateAdminSerializer,
)

from app_user.models import UserModel

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import (
    IsAuthenticatedPermission,
    IsAdminUserPermission,
    IsAdminSuperUserPermission,
)


class AdminListCreateAdminAPIView(generics.CustomListCreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsAdminSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminListAddUpdateAdminSerializer
    search_fields = ["username", "mobile_number", "first_name", "last_name"]

    def get_queryset(self):
        return UserModel.objects.filter(
            Q(is_staff=True) | Q(is_superuser=True)
        ).exclude(id=self.request.user.id)


class AdminUpdateDeleteAdminAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsAdminSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AdminListAddUpdateAdminSerializer
    object_name = "Admin"

    def get_queryset(self):
        return UserModel.objects.filter(
            Q(is_staff=True) | Q(is_superuser=True)
        ).exclude(id=self.request.user.id)
