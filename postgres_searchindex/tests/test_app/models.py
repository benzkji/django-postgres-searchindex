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
