from django.db import models
from django.core import validators


class PriceField(models.PositiveIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs["default"] = 0
        kwargs["validators"] = [validators.MinValueValidator(0)]
        super().__init__(*args, **kwargs)


class PercentField(models.FloatField):
    def __init__(self, *args, **kwargs):
        kwargs["default"] = 0
        kwargs["validators"] = [
            validators.MinValueValidator(0),
            validators.MaxValueValidator(100),
        ]
        super().__init__(*args, **kwargs)
