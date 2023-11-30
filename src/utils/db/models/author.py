from django.db import models


class AbstractAuthorModel(models.Model):
    class Meta:
        ordering = ["-id"]
        abstract = True

    # creator = models.ForeignKey(
    #     AdminModel,
    #     on_delete=models.SET_NULL,
    #     related_name="admin_article_creator",
    #     null=True,
    #     verbose_name=_("Admin Creator"),
    # )
    # editor = models.ForeignKey(
    #     AdminModel,
    #     on_delete=models.SET_NULL,
    #     related_name="admin_article_editor",
    #     null=True,
    #     verbose_name=_("Admin Editor"),
    # )
