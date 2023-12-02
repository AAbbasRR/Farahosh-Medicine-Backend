from django.core.validators import RegexValidator

from rest_framework.validators import UniqueValidator

from utils import BaseErrors

PhoneRegex = r"^{?(0?9[0-9]{9,9}}?)$"

PhoneNumberRegexValidator = RegexValidator(
    PhoneRegex, BaseErrors.invalid_mobile_number_format
)
