from django.db import models
from django.utils.translation import gettext as _

from utils.db.models import AbstractDateModel, AbstractAuthorModel
from utils.exceptions.core import MaximumDepthOfParentRelationshipExceededError


class CategoryManager(models.Manager):
    pass


class AbstractCategoryModel(AbstractDateModel, AbstractAuthorModel):
    class Meta:
        ordering = ["-id"]
        abstract = True

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
        verbose_name=_("Parent"),
    )
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name=_("Slug"))
    is_published = models.BooleanField(default=False, verbose_name=_("Is Published"))

    objects = CategoryManager()

    def __str__(self):
        full_path = [self.title]
        parent = self.parent
        while parent is not None:
            full_path.append(parent.title)
            parent = parent.parent
        return " -> ".join(full_path[::-1])

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        max_depth = 3
        if self.parent:
            depth = 1
            ancestor = self.parent
            while ancestor.parent:
                ancestor = ancestor.parent
                depth += 1
                if depth > max_depth:
                    raise MaximumDepthOfParentRelationshipExceededError()

        super().clean()
