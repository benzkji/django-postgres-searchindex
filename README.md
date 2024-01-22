# django-postgres-searchindex

[![CI](https://img.shields.io/github/actions/workflow/status/bnzk/django-postgres-searchindex/ci.yml?style=flat-square&logo=github "CI")](https://github.com/bnzk/django-postgres-searchindex/actions/workflows/ci.yml)
[![Version](https://img.shields.io/pypi/v/django-postgres-searchindex.svg?style=flat-square "Version")](https://pypi.python.org/pypi/django-postgres-searchindex/)
[![Licence](https://img.shields.io/github/license/bnzk/django-postgres-searchindex.svg?style=flat-square "Licence")](https://pypi.python.org/pypi/django-postgres-searchindex/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/django-postgres-searchindex?style=flat-square "PyPi Downloads")](https://pypistats.org/packages/django-postgres-searchindex)

A bit like django-haystack, but everything in postgres, accessible via Django ORM, using
postgres fullext search capabilites. The goal is to ease setup and 
maintainance for smaller and medium sized projects - without dependencies on
search technology like elastic, solr or whoosh.

During conception, I was thinking about developing a backend for django-haystack, but 
decided against, to be able to develop from the ground up, as simple as possible. The 
project could still provide a haystack backend one day, but it was just not my priority.

## Quickstart

Describe, index, search.

### Define index(es) in django settings

Default value, simplest possible configuration:

```
POSTGRES_SEARCHINDEX = {
    "default": {},
}
```

Example for a multilanguage setup:

```
POSTGRES_SEARCHINDEX = {
    "de": {
        "kwargs": {
            "language": "de",
        }
    },
    "fr": {
        "kwargs": {
            "language": "fr",
        }
    },
}
```

More complex configurations could include django's `SITE_ID` or other relevant infos
in searchindex key and kwargs.

### Define sources

Example, hopefully self explaining. Place this code in `index_sources.py` of your app, and
it will be autodiscovered.

```
from django.utils.html import strip_tags
from postgres_searchindex.base import IndexSource / MultiLanguageIndexSource
from postgres_searchindex.source_pool import source_pool

from news.models import News


@source_pool.register
class NewsIndexSource(IndexSource / MultiLanguageIndexSource):
    model = News

    def get_title(self, obj):
        return strip_tags(obj.description)

    def get_content(self, obj):
        return strip_tags(obj.description)

    def get_queryset(self):
        return self.model.objects.published()
```

### Populate the index

Run  `./manage.py postgres_searchindex_update` to update/build the index.

```
» ./manage.py postgres_searchindex_update
====================================
Updating index "de" with kwargs {'language': 'de'}
Person. Indexing 5 entries
> Done. Removed from index: 0
Project. Indexing 66 entries
> Done. Removed from index: 0
Media. Indexing 36 entries
> Done. Removed from index: 2
====================================
Updating index "fr" with kwargs {'language': 'fr'}
Person. Indexing 5 entries
> Done. Removed from index: 0
Project. Indexing 66 entries
> Done. Removed from index: 0
Media. Indexing 36 entries
> Done. Removed from index: 2
```

If you want to control how things were indexed, you can check
your `IndexEntry` instances in Django admin.

### Search!

You can now search in your index. You are free to use [Django's builtin fulltext](https://docs.djangoproject.com/en/dev/ref/contrib/postgres/search/)
features as you like - as in the following example, or in a way more advanced manner.

```
from django.contrib.postgres.search import SearchVector
from postgres_searchindex.models import IndexEntry

# this will return entries containing "überhaupt" and "uberhaupt"
IndexEntry.objects.annotate(
    search=SearchVector("content", "title", config="german")
).filter(index_key=self.request.LANGUAGE_CODE, search="uberhaupt")

```

There is a full example in the source: `views.py` and `urls.py` will give you an idea. 

To be done: |highlight:query templatefilter, to highlight the serach query in the 
search result text.

### Keep the index fresh

Either you'll regularly run `./manage.py postgres_searchindex_update`, or you'll 
implement a realtime or near realtime solution, with signals, throug the 
`POSTGRES_SEARCHINDEX_SIGNAL_PROCESSOR` setting. 

There are ~~two~~ currently one builtin processors:
 - `postgres_searchindex.signal_processors.RealtimeSyncedSignalProcessor`
 - To be done! `postgres_searchindex.signal_processors.RealtimeCelerySignalProcessor`

The async signal processor will require you to have celery configured.


## TODO

- properly handle removal of instances
- use trigram search?
- create an index for `content` and title
- instant update index via signals (update/delete models)
  - with celery? 
  - https://www.world-of-knives.ch/de/messershop/m-88-acier-japonais/
  - manage command: INdexEntry.objects.filter(original=None).delete() doesnt work?
    check each model...
