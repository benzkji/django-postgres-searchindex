from cms.models import CMSPlugin
from django.db import models
from django.urls import reverse


class TestModel(models.Model):
    published = models.BooleanField(default=True)
    title = models.CharField(
        max_length=255,
    )
    richtext = models.TextField(default="")
    richtext_second = models.TextField(default="")

    def __str__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        return reverse("testmodel_detail", args=(self.id,))


class TestPluginModel(CMSPlugin):
    field1 = models.CharField(max_length=64, default="", blank=False)
    field_date = models.DateField(
        default=None,
        null=True,
    )
    field_datetime = models.DateTimeField(
        default=None,
        null=True,
    )
    field_time = models.TimeField(
        default=None,
        null=True,
    )

    def __str__(self):
        return self.field1
