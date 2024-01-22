from django.utils.html import strip_tags

from postgres_searchindex.base import IndexSource
from postgres_searchindex.source_pool import source_pool

from .models import TestModel


@source_pool.register
class TestModelIndexSource(IndexSource):
    model = TestModel

    def get_title(self, obj):
        return obj.title

    def get_content(self, obj):
        return strip_tags(obj.richtext) + strip_tags(obj.richtext_second)

    def get_queryset(self):
        return self.model.objects.filter(published=True)
