from app_user.api.admin.serializers.change_password import AdminChangePasswordSerializer

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.permissions import IsAuthenticatedPermission, IsAdminUserPermission


class AdminChangePasswordAPIView(generics.CustomUpdateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    serializer_class = AdminChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
