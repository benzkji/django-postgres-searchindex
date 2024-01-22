from django.apps import AppConfig


class PostgresSearchIndexConfig(AppConfig):
    name = "postgres_searchindex"

    def ready(self):
        # discover all search indexes.
        from postgres_searchindex.source_pool import source_pool

        source_pool.discover()
