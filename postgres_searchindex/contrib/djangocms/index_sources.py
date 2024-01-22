from cms.models import Title
from django.db.models import Q
from django.utils import timezone

from postgres_searchindex.base import MultiLanguageIndexSource
from postgres_searchindex.contrib.djangocms.base import PlaceholderIndexSourceMixin
from postgres_searchindex.source_pool import source_pool


class TitleIndexSource(PlaceholderIndexSourceMixin, MultiLanguageIndexSource):
    model = Title

    def get_url(self, obj):
        return obj.page.get_absolute_url()

    def get_page_placeholders(self, page):
        """
        one day: allow specific configs, to include/exclude placeholders from indexing
        """
        return page.placeholders.all()

    def get_placeholder_content(self, obj, language, request):
        current_page = obj.page
        placeholders = self.get_page_placeholders(current_page)
        plugins = self.get_plugin_queryset(language).filter(
            placeholder__in=placeholders
        )
        text = ""
        for base_plugin in plugins:
            text = " " + self.get_plugin_search_text(base_plugin, request)

        return text

    def get_queryset(self):
        queryset = (
            Title.objects.public()
            .filter(
                Q(page__publication_date__lt=timezone.now())
                | Q(page__publication_date__isnull=True),
                Q(page__publication_end_date__gte=timezone.now())
                | Q(page__publication_end_date__isnull=True),
                Q(redirect__exact="") | Q(redirect__isnull=True),
                language=self.language,
            )
            .select_related("page")
        )
        # if GTE_CMS_35:
        queryset = queryset.select_related("page__node")
        return queryset.distinct()


source_pool.register(TitleIndexSource)
