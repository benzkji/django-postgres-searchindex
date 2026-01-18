from django.db.models import Q
from django.utils import timezone

from postgres_searchindex import conf
from postgres_searchindex.base import MultiLanguageIndexSource
from postgres_searchindex.contrib.djangocms.base import PlaceholderIndexSourceMixin
from postgres_searchindex.contrib.djangocms.compat import (
    GTE_CMS_35,
    GTE_CMS_50,
    LT_CMS_40,
)
from postgres_searchindex.source_pool import source_pool

# django CMS v4
try:
    from cms.models import PageContent
# django CMS 3.x
except ImportError:
    from cms.models import Title as PageContent


class PageContentIndexSource(PlaceholderIndexSourceMixin, MultiLanguageIndexSource):
    model = PageContent

    def get_url(self, obj):
        return obj.page.get_absolute_url()

    def get_page_placeholders(self, page, language):
        """
        one day: allow specific configs, to include/exclude placeholders from indexing
        """
        return page.get_placeholders(language)

    def get_site(self, obj):
        return obj.page.node.site

    def get_placeholder_content(self, obj, language, request):
        current_page = obj.page
        placeholders = self.get_page_placeholders(current_page, language)
        plugins = self.get_plugin_queryset(language).filter(
            placeholder__in=placeholders
        )
        text = ""
        for base_plugin in plugins:
            text += " " + self.get_plugin_search_text(base_plugin, request)
        return text

    def get_queryset(self):
        if LT_CMS_40:
            queryset = (
                PageContent.objects.public()
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
            queryset = queryset.select_related("page__node")
            queryset = queryset.distinct()
        else:
            from djangocms_versioning.constants import PUBLISHED

            queryset = PageContent.objects.filter(
                Q(versions__state=PUBLISHED),
                Q(redirect__exact="") | Q(redirect__isnull=True),
                language=self.language,
            ).select_related("page")
            if GTE_CMS_35 and not GTE_CMS_50:
                queryset = queryset.select_related("page__node").distinct()
        return queryset


TitleIndexSource = PageContentIndexSource

if conf.USE_CMS_INDEX:
    source_pool.register(PageContentIndexSource)
