from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class IndexEntryBase(models.Model):
    # meta fields
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    index_key = models.CharField(max_length=32, default="default")
    site_id = models.ForeignKey(
        "sites.Site",
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
    )
    # reference original
    # TODO: rename content_type to original_content_type and object_id to original_id?
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    original = GenericForeignKey("content_type", "object_id")
    original_modified_at = models.DateTimeField(default=timezone.now)

    # to be filled by apps/models
    title = models.CharField(
        max_length=1024,
    )
    content = models.TextField(default="")
    url = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class IndexEntry(IndexEntryBase):
    pass
