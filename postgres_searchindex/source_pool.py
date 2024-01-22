from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import autodiscover_modules

from postgres_searchindex.base import IndexSource
from postgres_searchindex.exceptions import (
    SourceAlreadyRegistered,
    SourceNotRegistered,
)
from postgres_searchindex.models import IndexEntry


class SourcePool:
    def __init__(self):
        self.sources = {}
        self.discovered = False

    def discover(self):
        if self.discovered:
            return
        autodiscover_modules("index_sources")
        self.discovered = True

    def clear(self):
        self.discovered = False
        self.sources = {}

    def register(self, source):
        """
        Registers the given search source.
        If an source is already registered, this will raise.
        """
        if not issubclass(source, IndexSource):
            raise ImproperlyConfigured(
                "Sources must be subclasses of postgres_searchindex.source.IndexSource,"
                " %r is not." % source
            )
        source_name = source.__name__
        if source_name in self.sources:
            raise SourceAlreadyRegistered(
                "Cannot register {!r}, an source with this name ({!r}) is already "
                "registered.".format(source, source_name)
            )
        # add generic relation to model
        related_query_name = (
            f"original_{source.model._meta.app_label}_{source.model._meta.model_name}"
        )
        source.model.add_to_class(
            "index_entries",
            GenericRelation(
                IndexEntry,
                related_query_name=related_query_name,
                content_type_field="content_type",
                object_id_field="object_id",
            ),
        )
        # add to registry
        self.sources[source_name] = source
        return source

    def unregister(self, source):
        """
        Unregisters the given source(s).

        If a source isn't already registered, this will raise sourceNotRegistered.
        """
        source_name = source.__name__
        if source_name not in self.sources:
            raise SourceNotRegistered("The source %r is not registered" % source)
        del self.sources[source_name]

    def get_sources(self):
        self.discover()
        return self.sources

    def get_source(self, name):
        """
        Retrieve a source from the cache.
        """
        self.discover()
        return self.sources[name]


source_pool = SourcePool()
