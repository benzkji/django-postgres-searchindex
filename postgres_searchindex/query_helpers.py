from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F

from postgres_searchindex import conf
from postgres_searchindex.models import IndexEntry


def basic_search(q, language_code):
    config = conf.LANGUAGE_2_PGCONFIG.get(language_code, "english")
    qs = (
        IndexEntry.objects.annotate(
            search=SearchVector(
                "content",
                "title",
                config=config,
            )
        )
        .filter(
            site_id=settings.SITE_ID,
            index_key=language_code,
            search=q,
        )
        .distinct()
    )
    return qs


def basic_search_with_ranking(q, language_code):
    config = conf.LANGUAGE_2_PGCONFIG.get(language_code, "english")
    search_vector = SearchVector("title", weight="A", config=config) + SearchVector(
        "content", weight="D", config=config
    )
    search_query = SearchQuery(q)
    qs = (
        IndexEntry.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query),
        )
        .filter(
            site_id=settings.SITE_ID,
            index_key=language_code,
            search=q,
        )
        .order_by("-rank")
        .distinct()
    )
    return qs


def basic_search_using_searchvector_index(q, language_code):
    qs = (
        IndexEntry.objects.annotate(rank=SearchRank(F("search_vector"), q))
        .filter(
            site_id=settings.SITE_ID,
            index_key=language_code,
            search_vector=q,
        )
        .order_by("-rank")
        .distinct()
    )
    return qs
