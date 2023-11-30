from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone

from utils.base_errors import BaseErrors


class AbstractVerificationModel(models.Model):
    class Meta:
        abstract = True

    class VerificationStatusOptions(models.TextChoices):
        pending = "pending", _("Pending")
        confirmed = "confirmed", _("Confirmed")
        rejected = "rejected", _("Rejected")

    verification_status = models.CharField(
        max_length=9,
        choices=VerificationStatusOptions.choices,
        default=VerificationStatusOptions.pending,
        verbose_name=_("Verification Status"),
    )
    verification_date = models.DateTimeField(
        null=True, verbose_name=_("Verification Date")
    )
    verification_description = models.TextField(
        null=True, blank=True, verbose_name=_("Verification Description")
    )

    def reset_verification(self):
        self.verification_status = self.VerificationStatusOptions.pending
        self.verification_date = None
        self.verification_description = None
        self.save()
