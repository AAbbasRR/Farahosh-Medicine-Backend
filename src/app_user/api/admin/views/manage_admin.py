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
    queryset = UserModel.objects.all(is_staff=True, is_superuser=True)


class AdminUpdateDeleteAdminAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsAdminSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AdminListAddUpdateAdminSerializer
    queryset = UserModel.objects.all(is_staff=True, is_superuser=True)
    object_name = "Admin"
