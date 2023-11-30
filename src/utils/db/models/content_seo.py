from django.db import models
from django.utils.translation import gettext as _
from django.utils.text import slugify


class AbstractContentSeoDataModel(models.Model):
    class Meta:
        ordering = ["-id"]
        abstract = True

    title = models.CharField(max_length=100, verbose_name=_("Title"))
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name=_("Slug"))
    content = models.TextField(verbose_name=_("Content"))
    short_description = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Short Description")
    )
    meta_description = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_("Meta Description")
    )
    keywords = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Keywords"),
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug, allow_unicode=True)
        return super().save(*args, **kwargs)
