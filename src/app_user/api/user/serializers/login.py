from rest_framework import serializers

from app_user.models import UserModel

from utils.serializers import (
    CustomModelSerializer,
    CustomSerializer,
)
from utils.db.validators import PhoneNumberRegexValidator
from utils.exceptions.core import (
    ObjectNotFoundError,
    RedisKeyNotExistsError,
)
from utils.exceptions.rest import (
    NotFoundObjectException,
    OtpCodeExpiredOrNotFoundException,
    UserOtpCodeVerifyLockedException,
    UserAccountIsNotActiveException,
)
from utils.base_errors import BaseErrors


class UserLoginSerializer(CustomModelSerializer):
    mobile_number = serializers.CharField(
        required=True,
        validators=[
            PhoneNumberRegexValidator,
        ],
    )

    class Meta:
        model = UserModel
        fields = ("mobile_number",)

    def validate(self, attrs):
        try:
            user_obj = UserModel.objects.find_by_mobile_number(**attrs)
            if user_obj.is_active is False:
                raise UserAccountIsNotActiveException()
            user_obj.send_otp_code_to_mobile_number("login")
            return attrs
        except ObjectNotFoundError:
            raise NotFoundObjectException(object_name="User")


class UserVerifyLoginOtpSerializer(CustomSerializer):
    mobile_number = serializers.CharField(
        required=True,
        validators=[
            PhoneNumberRegexValidator,
        ],
    )
    otp_code = serializers.IntegerField(
        required=True,
    )

    def validate(self, attrs):
        try:
            user_obj = UserModel.objects.find_by_mobile_number(attrs["mobile_number"])
            if user_obj.check_has_perm_for_try_otp_code(
                field_verify="mobile_number", ip=self.client_ip
            ):
                try:
                    user_validate_otp_code_result = user_obj.verify_user_otp_code(
                        attrs["otp_code"],
                        field_verify="mobile_number",
                        ip=self.client_ip,
                    )
                    if user_validate_otp_code_result is True:
                        user_obj.set_last_login()
                        return user_obj.user_login_detail()
                    else:
                        raise serializers.ValidationError(
                            {"otp_code": BaseErrors.invalid_otp_code}
                        )
                except RedisKeyNotExistsError:
                    raise OtpCodeExpiredOrNotFoundException()
            else:
                raise UserOtpCodeVerifyLockedException()
        except ObjectNotFoundError:
            raise NotFoundObjectException(object_name="User")
