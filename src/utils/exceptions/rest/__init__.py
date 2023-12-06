from django.utils.translation import gettext as _

from rest_framework.exceptions import (
    APIException,
    _get_error_details,
)

from utils.base_errors import BaseErrors


class InvalidUsernameOrPasswordException(APIException):
    status_code = 400
    default_detail = BaseErrors.invalid_username_or_password


class UserNotAdminException(APIException):
    status_code = 400
    default_code = BaseErrors.user_is_not_admin


class OldPasswordIsIncorrectException(APIException):
    status_code = 400

    def __init__(
        self, detail=BaseErrors.old_password_is_incorrect, field_name="old_password"
    ):
        super().__init__(detail={field_name: detail})


class NotFoundObjectException(APIException):
    status_code = 404

    def __init__(self, detail=BaseErrors.object_not_found, object_name=None):
        if object_name is not None:
            detail = BaseErrors.change_error_variable(
                "object_not_found", object=_(object_name)
            )
        super().__init__(detail)


class OtpCodeExpiredOrNotFoundException(APIException):
    status_code = 400
    default_detail = BaseErrors.otp_code_expired


class UserOtpCodeVerifyLockedException(APIException):
    status_code = 423
    default_detail = BaseErrors.too_much_effort


class ParameterRequiredException(APIException):
    status_code = 400

    def __init__(self, params=None):
        if params is None:
            params = ["pk"]
        detail = BaseErrors.change_error_variable(
            "parameter_is_required", param_name=" or ".join(params)
        )
        super().__init__(detail)


class UserAccountIsNotActiveException(APIException):
    status_code = 406

    def __init__(self, detail=None):
        if detail is None:
            detail = BaseErrors.user_account_not_active

        if isinstance(detail, dict):
            detail["detail"] = BaseErrors.user_account_not_active

        self.detail = _get_error_details(detail, self.status_code)
