from app_user.api.user.serializers.login import (
    UserLoginSerializer,
    UserVerifyLoginOtpSerializer,
)

from utils.views import generics
from utils.views.permissions import AllowAnyPermission
from utils.views.versioning import BaseVersioning


class UserLoginAPIView(generics.CustomGenericPostAPIView):
    permission_classes = [
        AllowAnyPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = UserLoginSerializer


class UserVerifyLoginOtpAPIView(generics.CustomGenericPostAPIView):
    permission_classes = [
        AllowAnyPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = UserVerifyLoginOtpSerializer
