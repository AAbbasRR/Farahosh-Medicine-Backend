from app_user.models import UserModel

from utils.serializers import CustomModelSerializer
from utils.exceptions.core import InvalidUsernameOrPasswordError
from utils.exceptions.rest import (
    InvalidUsernameOrPasswordException,
    UserNotAdminException,
)


class AdminLoginSerializer(CustomModelSerializer):
    class Meta:
        model = UserModel
        fields = ("username", "password")
        extra_kwargs = {"username": {"validators": []}}

    def validate(self, attrs):
        try:
            user_obj = UserModel.objects.authenticate_user(**attrs)
            if False in [user_obj.is_staff, user_obj.is_superuser]:
                raise UserNotAdminException()
            user_obj.set_last_login()
            return user_obj.user_login_detail()
        except InvalidUsernameOrPasswordError:
            raise InvalidUsernameOrPasswordException()
