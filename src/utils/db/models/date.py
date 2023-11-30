from django.db import models
from django.utils.translation import gettext as _
from django.core.management import settings


class AbstractDateModel(models.Model):
    class Meta:
        abstract = True
        ordering = ["create_at"]

    create_at = models.DateTimeField(verbose_name=_("Created Time"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated Time"), auto_now=True)

    def formatted_create_at(self):
        return self.create_at.strftime(
            f"{settings.DATE_INPUT_FORMATS} {settings.TIME_INPUT_FORMATS}"
        )

    def formatted_updated_at(self):
        return self.updated_at.strftime(
            f"{settings.DATE_INPUT_FORMATS} {settings.TIME_INPUT_FORMATS}"
        )
