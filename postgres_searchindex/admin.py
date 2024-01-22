from django.contrib import admin

from .models import IndexEntry


@admin.register(IndexEntry)
class IndexEntryAdmin(admin.ModelAdmin):
    list_display_links = ("title",)
    list_display = (
        "index_key",
        "title",
        "url",
        "modified_at",
    )
    search_fields = ("title", "content")
    list_filter = (
        "index_key",
        "content_type",
    )
