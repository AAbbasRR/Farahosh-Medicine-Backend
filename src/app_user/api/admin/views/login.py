from app_user.api.admin.serializers.login import AdminLoginSerializer

from utils.views import generics
from utils.views.permissions import AllowAnyPermission
from utils.views.versioning import BaseVersioning


class AdminLoginAPIView(generics.CustomGenericPostAPIView):
    permission_classes = [
        AllowAnyPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AdminLoginSerializer
