from django.conf import settings

# index config
POSTGRES_SEARCHINDEX = getattr(
    settings,
    "POSTGRES_SEARCHINDEX",
    {
        "default": {},
    },
)

# search view
QUERY_FUNC = getattr(
    settings,
    "POSTGRES_SEARCHINDEX_QUERY_FUNC",
    "postgres_searchindex.helpers.basic_search_using_searchvector",
)
SEARCH_VECTOR_FUNC = getattr(
    settings,
    "POSTGRES_SEARCHINDEX_SEARCH_VECTOR_FUNC",
    "postgres_searchindex.helpers.update_search_vector_weighted_a_d",
)
LANGUAGE_2_PGCONFIG = getattr(
    settings,
    "POSTGRES_SEARCHINDEX_LANGUAGE_2_PGCONFIG",
    {
        "en": "english",
        "de": "german",
        "fr": "french",
    },
)
PAGINATE_BY = getattr(
    settings,
    "POSTGRES_SEARCHINDEX_PAGINATE_BY",
    20,
)

# contrib.djangocms
USE_CMS_INDEX = getattr(
    settings,
    "POSTGRES_SEARCHINDEX_USE_CMS_INDEX",
    True,
)
