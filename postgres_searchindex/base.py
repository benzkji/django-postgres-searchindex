from django.utils.translation import override

from postgres_searchindex.models import IndexEntry

# IndexEntry = apps.get_model("postgres_searchindex", "IndexEntry", require_ready=False)


class IndexSource:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_queryset(self):
        return self.model.objects.all()

    def get_related_query_name(self):
        related_query_name = self.model.index_entries.field.related_query_name()
        return related_query_name

    def get_data(self, obj):
        data = {
            "id": obj.id,
            "title": self.get_title(obj),
            "content": self.get_content(obj),
            "url": self.get_url(obj),
        }
        return data

    def update(self, index_key, obj):
        kwargs = {self.get_related_query_name(): obj}
        # why not get_or_create? because generic foreign key.
        try:
            index_entry = IndexEntry.objects.get(index_key=index_key, **kwargs)
        except IndexEntry.DoesNotExist:
            index_entry = obj.index_entries.create(index_key=index_key)
        data = self.get_data(obj)
        index_entry.title = data["title"]
        index_entry.content = str(data["content"])
        index_entry.url = data["url"]
        index_entry.save()

    def get_title(self, obj):
        return getattr(obj, "title", "")

    def get_content(self, obj):
        return getattr(obj, "content", "")

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_json(self, obj):
        pass


class MultiLanguageIndexSource(IndexSource):
    def __init__(self, **kwargs):
        self.language = kwargs.pop("language")
        self.kwargs = kwargs

    def get_data(self, obj):
        with override(self.language):
            data = super().get_data(obj)
            return data
