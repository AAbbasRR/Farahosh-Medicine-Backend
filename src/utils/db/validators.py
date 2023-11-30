from django.core.validators import RegexValidator

from rest_framework.validators import UniqueValidator

from utils import BaseErrors

PhoneRegex = r"^{?(0?9[0-9]{9,9}}?)$"
EmailRegex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

PhoneNumberRegexValidator = RegexValidator(
    PhoneRegex, BaseErrors.invalid_mobile_number_format
)

EmailRegexValidator = RegexValidator(EmailRegex, BaseErrors.invalid_email_format)
