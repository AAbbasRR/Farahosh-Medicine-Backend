from django.db import models
from django.conf import settings
from django.core import validators

from utils.exceptions.core import InvalidValueError

from decimal import Decimal
import hashlib


class CustomFileField(models.FileField):
    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)

        return file


class CustomImageField(models.ImageField):
    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)

        return file


class PriceField(models.PositiveIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs["default"] = 0
        kwargs["validators"] = [validators.MinValueValidator(0)]
        super().__init__(*args, **kwargs)


class PercentField(models.PositiveIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs["default"] = 0
        kwargs["validators"] = [
            validators.MinValueValidator(0),
            validators.MaxValueValidator(100),
        ]
        super().__init__(*args, **kwargs)
