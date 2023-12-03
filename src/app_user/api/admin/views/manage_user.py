from app_user.api.admin.serializers.manage_user import AdminListAddUpdateUserSerializer

from app_user.models import UserModel

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import IsAuthenticatedPermission, IsAdminUserPermission


class AdminListCreateUserAPIView(generics.CustomListCreateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminListAddUpdateUserSerializer
    search_fields = ["mobile_number", "first_name", "last_name"]
    queryset = UserModel.objects.all(is_staff=False, is_superuser=False)


class AdminUpdateDeleteUserAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    serializer_class = AdminListAddUpdateUserSerializer
    queryset = UserModel.objects.all(is_staff=False, is_superuser=False)
    object_name = "User"
