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
    old_password_is_incorrect = _("Old Password Is Incorrect")
    invalid_mobile_number_format = _("Invalid Mobile Number Format")
    passwords_do_not_match = _("Passwords do not match.")
    invalid_username_or_password = _("Invalid Email Or Password.")
    user_account_not_active = _("User Account Not Active.")

    # otp code validate
    otp_code_expired = _("OTP Code Expired, Please Try To Resend New OTP Code.")
    too_much_effort = _(
        "Too Much Effort. You Are Not Allowed To Send Request Minutes, Please Try Again Later"
    )
    invalid_otp_code = _("Invalid OTP Code, Please Try Again.")

    # global
    parameter_is_required = _("parameter {param_name} is required")
    object_do_not_have_attribute = _("{object} Do Not Have {attribute}")
    object_not_found = _("{object} Not Found")

    # permissions
    # admin
    user_is_not_admin = _("User Is Not Admin")
