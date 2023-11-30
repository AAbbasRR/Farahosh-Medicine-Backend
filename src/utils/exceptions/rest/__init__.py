from django.utils.translation import gettext as _

from rest_framework.exceptions import (
    APIException,
    ValidationError,
    _get_error_details,
)

from utils.base_errors import BaseErrors


class InvalidUsernameOrPasswordException(APIException):
    status_code = 400
    default_detail = BaseErrors.invalid_username_or_password


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


class OtpHasAlreadyBenSentException(APIException):
    status_code = 400
    default_detail = BaseErrors.otp_code_has_already_been_sent


class UserMobileNumberVerifiedException(APIException):
    status_code = 400
    default_detail = BaseErrors.mobile_number_verified


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


class CantCreateCommentException(APIException):
    status_code = 400
    default_detail = BaseErrors.cant_create_comment


class UserAccountIsNotActiveException(APIException):
    status_code = 406

    def __init__(self, detail=None):
        if detail is None:
            detail = BaseErrors.user_account_not_active

        if isinstance(detail, dict):
            detail["detail"] = BaseErrors.user_account_not_active

        self.detail = _get_error_details(detail, self.status_code)


class InvalidFieldValueException(ValidationError):
    status_code = 400

    def __init__(self, field_name):
        detail = {field_name: BaseErrors.invalid_field_value}
        super().__init__(detail)


class UserAccountIsActivateException(APIException):
    status_code = 400
    default_detail = BaseErrors.user_account_is_active


class MaximumDepthOfParentRelationshipExceededException(APIException):
    status_code = 400

    def __init__(self, detail=None, max_depth=3):
        if detail is None:
            detail = BaseErrors.change_error_variable(
                "maximum_depth_parent_child_relationship", depth=max_depth
            )
        super().__init__(detail)


class InvalidMobileOrEmailFormatException(APIException):
    status_code = 400
    default_detail = BaseErrors.invalid_mobile_number_or_email_format


class DoNotHaveResetPasswordPermissionException(APIException):
    status_code = 400
    default_detail = BaseErrors.user_dont_have_forget_password_permission


class ProblemOnlinePaymentGatewayException(APIException):
    status_code = 400
    default_detail = BaseErrors.error_in_payment_gateway


class DepositFailedException(APIException):
    status_code = 400
    default_detail = BaseErrors.deposit_failed


class DepositInvalidStatusValueException(APIException):
    status_code = 400
    default_detail = BaseErrors.invalid_status_value


class DepositPaymentTimeExpiredException(APIException):
    status_code = 400
    default_detail = BaseErrors.payment_time_expired


class BankCardNotConfirmedException(APIException):
    status_code = 400
    default_detail = BaseErrors.bank_card_not_confirmed


class MinimumWithdrawalAmountException(APIException):
    status_code = 400

    def __init__(self, amount=0):
        detail = BaseErrors.change_error_variable(
            "withdrawal_minimum_amount", amount=amount
        )
        super().__init__(detail)


class UserWalletBalanceNotEnoughException(APIException):
    status_code = 400
    default_detail = BaseErrors.balance_not_enough


class ProductInventoryNotEnoughException(APIException):
    status_code = 400
    default_detail = BaseErrors.product_inventory_not_enough


class UserCartIsEmptyException(APIException):
    status_code = 400
    default_detail = BaseErrors.your_cart_has_empty


class CartCouponMinimumPurchaseException(APIException):
    status_code = 400

    def __init__(self, minimum_purchase=0):
        detail = BaseErrors.change_error_variable(
            "minimum_order_must_value", value=minimum_purchase
        )
        super().__init__(detail)


class MaximumMarketProductDiscountException(APIException):
    status_code = 400

    def __init__(self, maximum_percent):
        detail = BaseErrors.change_error_variable(
            "the_product_discount_not_valid", percent=maximum_percent
        )
        super().__init__(detail)
