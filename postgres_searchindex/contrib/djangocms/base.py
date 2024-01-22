from cms.models import CMSPlugin

from postgres_searchindex.contrib.djangocms.helpers import (
    get_plugin_index_content,
    get_request,
)


class PlaceholderIndexSourceMixin:
    """
    helper mixin, for easier indexing of placeholderfields
    use MultiLanguageIndexSource as source base class when using this mixin
    """

    def get_content(self, obj):
        request = get_request(self.language)
        return self.get_placeholder_content(obj, self.language, request)

    def get_plugin_queryset(self, language):
        queryset = CMSPlugin.objects.filter(language=language)
        return queryset

    def get_placeholder_content(self, obj, language, request):
        placeholder = getattr(obj, self.placeholder_field_name, "content")
        plugins = self.get_plugin_queryset(language).filter(placeholder=placeholder)
        text = ""
        for base_plugin in plugins:
            text += self.get_plugin_search_text(base_plugin, request)
        return text

    def get_plugin_search_text(self, base_plugin, request):
        plugin_content = get_plugin_index_content(base_plugin, request)
        return plugin_content.strip()
