from django.utils.translation import gettext as _


class BaseErrors:
    @classmethod
    def change_error_variable(cls, error_name, **kwargs):
        message = getattr(cls, error_name)
        for key, value in kwargs.items():
            message = message.replace("{%s}" % key, str(value))
        return message

    @classmethod
    def return_error_with_name(cls, error_name):
        return getattr(cls, error_name)

    # project
    url_not_found = _("URL Not Found.")
    server_error = _("Server Error.")

    # public sign up, login, forget pass, change pass
    invalid_mobile_number_format = _("Invalid Mobile Number Format")
    invalid_email_format = _("Invalid Email Format")
    invalid_mobile_number_or_email_format = _("Invalid Mobile Number Or Email Format")
    mobile_number_verified = _("Your Mobile Number Is Verified")
    passwords_do_not_match = _("Passwords do not match.")
    invalid_username_or_password = _("Invalid Email Or Password.")
    user_account_not_active = _("User Account Not Active.")
    user_account_is_active = _("User Account Is Active.")
    user_dont_have_forget_password_permission = _(
        "You Do Not Have Access To Change The Password, Please Try Again First Step."
    )

    # otp code validate
    otp_code_expired = _("OTP Code Expired, Please Try To Resend New OTP Code.")
    too_much_effort = _(
        "Too Much Effort. You Are Not Allowed To Send Request Minutes, Please Try Again Later"
    )
    invalid_otp_code = _("Invalid OTP Code, Please Try Again.")
    otp_code_has_already_been_sent = _("OTP Code Has Already Been Sent.")

    # customer and user
    you_have_verified_mobile_number = _("You Verified Your Mobile Number")
    you_have_verified_email = _("You Verified Your Email")
    cant_update_profile_data = _("Cant Update Verified Profile Data")

    # comment
    cant_create_comment = _("Cant Create Comment")

    # wallet
    balance_not_enough = _("Balance Not Enough")

    # cart
    product_inventory_not_enough = _("Product Inventory Not Enough")

    # order
    your_cart_has_empty = _("Your Cart Has Empty")

    # deposit
    error_in_payment_gateway = _("Problem In The Payment Gateway System")
    deposit_failed = _("Deposit Failed")
    invalid_status_value = _("Invalid Status Value [OK, NOK]")
    payment_time_expired = _("Deposit Failed, Payment Time Expired")
    the_amount_may_not_be_greater_than_1000000000 = _(
        "The Amount May Not Be Greater Than 100000000"
    )

    # withdraw
    bank_card_not_confirmed = _("Bank Card Not Confirmed")
    withdrawal_minimum_amount = _("Minimum Withdrawal Amount is {amount}")

    # global
    parameter_is_required = _("parameter {param_name} is required")
    object_do_not_have_attribute = _("{object} Do Not Have {attribute}")
    object_not_found = _("{object} Not Found")
    minimum_order_must_value = _("The Minimum Order Amount Must Be {value}")
    maximum_depth_parent_child_relationship = _(
        "The Category Cannot Be More Than {depth} Layers"
    )
    required_field_with_type = _(
        "This field is required for attributes with type '{type}'"
    )
    invalid_field_value = _("Invalid Value")
    the_product_discount_not_valid = _(
        "The Maximum Product Discount Should Be {percent}"
    )

    # permissions
    # admin
    user_is_not_admin = _("User Is Not Admin")
    # user
    user_is_not_seller = _("User Is Not Seller")
    # customer
    user_is_not_customer = _("User Is Not Customer")
