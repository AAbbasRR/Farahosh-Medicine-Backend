from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    update_last_login,
)
from django.db import models, transaction
from django.utils.translation import gettext as _
from django.core.management import settings

from rest_framework_simplejwt.tokens import RefreshToken

from utils.base_errors import BaseErrors
from utils.db.validators import PhoneNumberRegexValidator
from utils.classes import (
    Redis,
    ManageSMSPortal,
)
from utils.data_list import RedisKeys
from utils.exceptions.core import (
    ObjectNotFoundError,
    RedisKeyNotExistsError,
    InvalidUsernameOrPasswordError,
)


class UserMobileNumberManager(models.Manager):
    def find_by_mobile_number(self, mobile_number, **kwargs):
        try:
            return self.get(mobile_number=mobile_number, **kwargs)
        except self.model.DoesNotExist:
            raise ObjectNotFoundError()


class UserManager(BaseUserManager, UserMobileNumberManager):
    def authenticate_user(self, username, password, **kwargs):
        try:
            user_obj = self.get(username=username, **kwargs)
            if user_obj.check_password(password):
                return user_obj
            else:
                raise InvalidUsernameOrPasswordError()
        except self.model.DoesNotExist:
            raise InvalidUsernameOrPasswordError()

    def create_user(self, username, password=None, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password):
        user = self.model(
            email=username,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def register_user(self, username, password=None, **kwargs):
        with transaction.atomic():
            user = self.create_user(username, password, **kwargs)
        return user


class UserMobileNumber(models.Model):
    class Meta:
        abstract = True

    mobile_number = models.CharField(
        max_length=11,
        validators=[PhoneNumberRegexValidator],
        unique=True,
        verbose_name=_("Mobile Number"),
    )

    def send_otp_code_to_mobile_number(self, title_type):
        """
        create a otp code and send to public mobile number
        """
        if self.mobile_number is not None:
            sms_service = ManageSMSPortal(self.mobile_number)
            sms_service.send_otp_code(title_type)
        else:
            raise AttributeError(
                BaseErrors.change_error_variable(
                    "object_do_not_have_attribute",
                    object="User",
                    attribute="mobile_number",
                )
            )

    def check_otp_code_to_mobile_number_existed(self, title_type):
        if self.mobile_number is not None:
            sms_service = ManageSMSPortal(self.mobile_number)
            return sms_service.check_otp_code_existed(title_type)
        else:
            raise AttributeError(
                BaseErrors.change_error_variable(
                    "object_do_not_have_attribute",
                    object="User",
                    attribute="mobile_number",
                )
            )

    def check_validity_previous_otp(self, field_verify, custom_value=None):
        value = ""
        if custom_value is None:
            if getattr(self, field_verify) is not None:
                value = getattr(self, field_verify)
            else:
                raise AttributeError(
                    BaseErrors.return_error_with_name(f"user_must_have_{field_verify}")
                )
        else:
            value = custom_value
        redis_user_otp_code_cache_service = Redis(f"{value}", RedisKeys.verify_otp_code)
        return redis_user_otp_code_cache_service.exists()

    def verify_user_otp_code(
        self,
        raw_otp_code,
        field_verify,
        lock_user_when_wrong_code=True,
        ip=None,
        custom_value=None,
    ):
        value = ""
        if custom_value is None:
            value = getattr(self, field_verify)
        else:
            value = custom_value
        redis_user_otp_code_cache_service = Redis(f"{value}", RedisKeys.verify_otp_code)
        redis_lock_wrong_try_cache_service = Redis(
            f"{value}-{ip}",
            RedisKeys.lock_wrong_try_otp_code_verify,
        )

        otp_code_validate_result = redis_user_otp_code_cache_service.validate(
            raw_otp_code
        )
        match otp_code_validate_result:
            case None:
                raise RedisKeyNotExistsError()
            case True:
                redis_lock_wrong_try_cache_service.delete()
                redis_user_otp_code_cache_service.delete()
            case False:
                if lock_user_when_wrong_code is True:
                    try:
                        try_count = redis_lock_wrong_try_cache_service.get_value()
                        redis_lock_wrong_try_cache_service.set_value(try_count + 1)
                    except TypeError:
                        redis_lock_wrong_try_cache_service.set_value(1)
                    redis_lock_wrong_try_cache_service.set_expire(
                        RedisKeys.lock_wrong_try_otp_code_verify_expire
                    )
        return otp_code_validate_result

    def check_has_perm_for_try_otp_code(self, field_verify, ip=None, custom_value=None):
        value = ""
        if custom_value is None:
            value = getattr(self, field_verify)
        else:
            value = custom_value
        redis_lock_wrong_try_cache_service = Redis(
            f"{value}-{ip}",
            RedisKeys.lock_wrong_try_otp_code_verify,
        )
        try:
            user_try_count = redis_lock_wrong_try_cache_service.get_value()
            if user_try_count >= settings.MAXIMUM_COUNT_TRY_WRONG_OTP_CODE:
                return False
            else:
                return True
        except TypeError:
            return True


class User(AbstractUser, UserMobileNumber):
    email = None

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.pk} {self.mobile_number}"

    def formatted_last_login(self):
        if self.last_login is None:
            return None
        return self.last_login.strftime(
            f"{settings.DATE_INPUT_FORMATS} {settings.TIME_INPUT_FORMATS}"
        )

    def formatted_date_joined(self):
        return self.date_joined.strftime(
            f"{settings.DATE_INPUT_FORMATS} {settings.TIME_INPUT_FORMATS}"
        )

    def set_last_login(self):
        """
        :return: When the public logs in, we record her login time as the last login time
        """
        update_last_login(None, self)
        return self

    def create_new_token(self):
        """
        create new token for public object with jwt
        return:{
            refresh: jwt refresh token,
            access: jwt access token with 5 minute time life
        }
        """
        refresh_token = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token),
        }

    def user_info(self, user_type="User"):
        return {
            "mobile_number": self.mobile_number,
            "date_joined": self.formatted_date_joined(),
            "last_login": self.formatted_last_login(),
            "full_name": self.get_full_name(),
            "is_staff": self.is_staff,
            "is_superuser": self.is_superuser,
        }

    def user_login_detail(self):
        user_info = self.user_info()
        user_info.update(
            {
                "token": self.create_new_token(),
            }
        )
        return user_info
