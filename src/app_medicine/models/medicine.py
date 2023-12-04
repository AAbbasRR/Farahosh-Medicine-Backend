from django.db import models
from django.utils.translation import gettext as _

from utils.db.models import AbstractDateModel
from utils.db import fields


class Medicine(AbstractDateModel):
    class ShapeOptions(models.TextChoices):
        UN = "UN", _("UN")
        TAB = "TAB", _("TAB")
        TAB_DELAYED_RELEASE = "TAB_DELAYED_RELEASE", _("TAB DELAYED RELEASE")
        INJ = "INJ", _("INJ")
        ORAL_SOL = "ORAL_SOL", _("ORAL SOL")
        ORAL_SUSP = "ORAL_SUSP", _("ORAL SUSP")
        POWDER = "POWDER", _("POWDER")
        DROP = "DROP", _("DROP")
        CAP = "CAP", _("CAP")
        SOLUTION = "SOLUTION", _("SOLUTION")
        INHALATION = "INHALATION", _("INHALATION")
        SYRUP = "SYRUP", _("SYRUP")
        POWDER_FOR_INJ = "POWDER_FOR_INJ", _("POWDER_FOR_INJ")
        INJ_POWDER = "INJ_POWDER", _("INJ_POWDER")

    brand_code = models.CharField(max_length=5, verbose_name=_("Brand Code"))
    title = models.CharField(max_length=124, verbose_name=_("Title"))
    term = models.TextField(null=True, blank=True, verbose_name=_("Term"))
    shape = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_("Shape")
    )
    dose = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_("Dose")
    )
    price_exchange_subsidy = fields.PriceField(
        verbose_name=_("Total Price Including Foreign Exchange Subsidy")
    )
    percent_share_of_organization_exchange_subsidy = fields.PercentField(
        verbose_name=_(
            "Percent Share Of The Organization Including Foreign Exchange Subsidy"
        )
    )

    def price_of_percent_organization(self):
        return self.price_exchange_subsidy * (
            self.percent_share_of_organization_exchange_subsidy / 100
        )

    def get_full_name(self):
        return f"{self.title} - {self.shape} - {self.dose}"
