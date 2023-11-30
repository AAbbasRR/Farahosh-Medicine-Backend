from django.db import models
from django.apps import apps
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.management import settings

from utils.exceptions.core import MaximumDepthOfParentRelationshipExceededError
from utils.db.models import AbstractDateModel

CUSTOMER_MODEL = "app_customer.CustomerProfile"
RESELLER_MODEL = "app_reseller.ResellerProfile"


class AbstractCommentModel(AbstractDateModel):
    class Meta:
        ordering = ["-id"]
        abstract = True

    class AuthorTypeOptions(models.TextChoices):
        Admin = "Admin", _("Admin")
        Customer = "Customer", _("Customer")
        Reseller = "Reseller", _("Reseller")

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replays",
        verbose_name=_("Parent"),
    )
    author_type = models.CharField(
        max_length=8,
        choices=AuthorTypeOptions.choices,
        default=AuthorTypeOptions.Customer,
        verbose_name=_("Author Type"),
    )
    author_id = models.PositiveIntegerField(verbose_name=_("Author ID"))
    message = models.TextField(verbose_name=_("Message"))
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        verbose_name=_("Score"),
    )
    is_verified = models.BooleanField(default=False, verbose_name=_("Is Verified"))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self, max_depth=2):
        if self.parent:
            depth = 1
            ancestor = self.parent
            while ancestor.parent:
                ancestor = ancestor.parent
                depth += 1
                if depth > max_depth:
                    raise MaximumDepthOfParentRelationshipExceededError(max_depth)

        super().clean()

    @property
    def author_name(self):
        match self.author_type:
            case self.AuthorTypeOptions.Admin:
                return _(f"{settings.PROJECT_NAME} Support")
            case self.AuthorTypeOptions.Customer:
                try:
                    customer_model_path = CUSTOMER_MODEL.split(".")
                    customer_profile_model = apps.get_model(
                        customer_model_path[0], customer_model_path[1]
                    )
                    customer_profile = customer_profile_model.objects.get(
                        pk=self.author_id
                    )
                    author_full_name = customer_profile.full_name
                    return (
                        author_full_name if author_full_name != " " else _("Anonymous")
                    )
                except customer_profile_model.DoesNotExist:
                    return _("Anonymous")

    @property
    def author_detail(self):
        author_detail = {
            "type": self.author_type,
            "id": self.author_id,
        }
        match self.author_type:
            case self.AuthorTypeOptions.Admin:
                author_detail.update(
                    {
                        "name": _(f"{settings.PROJECT_NAME} Support"),
                        "email": _(f"{settings.PROJECT_NAME} Support"),
                        "mobile_number": _(f"{settings.PROJECT_NAME} Support"),
                    }
                )
            case self.AuthorTypeOptions.Customer:
                try:
                    customer_model_path = CUSTOMER_MODEL.split(".")
                    customer_profile_model = apps.get_model(
                        customer_model_path[0], customer_model_path[1]
                    )
                    customer_profile = customer_profile_model.objects.get(
                        user_id=self.author_id
                    )
                    author_detail.update(
                        {
                            "name": customer_profile.full_name
                            if customer_profile.full_name != " "
                            else _("Anonymous"),
                            "email": customer_profile.user.email,
                            "mobile_number": customer_profile.user.mobile_number,
                        }
                    )
                except customer_profile_model.DoesNotExist:
                    return author_detail.update(
                        {"name": None, "email": None, "mobile_number": None}
                    )
        return author_detail


class AbstractCommentReactionModel(AbstractDateModel):
    class Meta:
        ordering = ["-id"]
        abstract = True

    class AuthorTypeOptions(models.TextChoices):
        Admin = "Admin", _("Admin")
        Customer = "Customer", _("Customer")
        Reseller = "Reseller", _("Reseller")

    is_liked = models.BooleanField(default=True, verbose_name=_("Is Liked"))
    author_type = models.CharField(
        max_length=8,
        choices=AuthorTypeOptions.choices,
        default=AuthorTypeOptions.Customer,
        verbose_name=_("Author Type"),
    )
    author_id = models.PositiveIntegerField(verbose_name=_("Author ID"))
