import sys

from django.contrib.contenttypes.models import ContentType

from postgres_searchindex import conf
from postgres_searchindex.models import IndexEntry
from postgres_searchindex.source_pool import source_pool


def delete_indexes():
    IndexEntry.objects.all().delete()


def update_indexes():
    for index_key, index in conf.POSTGRES_SEARCHINDEX.items():
        sys.stdout.write("====================================")
        sys.stdout.write(
            f"Updating index \"{index_key}\" with kwargs {index.get('kwargs', {})}"
        )
        for source_cls in source_pool.get_sources().values():
            source = source_cls(**index.get("kwargs", {}))
            sys.stdout.write(
                f"{source.model.__name__}. "
                f"Indexing {source.get_queryset().count()} entries"
            )
            # index
            current_ids = []
            for obj in source.get_queryset():
                source.update(index_key, obj)
                current_ids.append(obj.id)
            # remove no more existing
            content_type = ContentType.objects.get_for_model(source.model)
            to_delete = IndexEntry.objects.filter(
                index_key=index_key,
                content_type=content_type,
            ).exclude(
                object_id__in=current_ids,
            )
            delete_result = to_delete.delete()
            sys.stdout.write(f"> Done. Removed from index: {delete_result[0]}")
