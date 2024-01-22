from django.conf import settings
from django.core.management import BaseCommand
from django.contrib.contenttypes.models import ContentType

from postgres_searchindex.models import IndexEntry
from postgres_searchindex.source_pool import source_pool


class Command(BaseCommand):
    help = "Update/build index"

    def handle(self, *args, **options):
        for index_key, index in settings.POSTGRES_SEARCHINDEX.items():
            self.stdout.write("====================================")
            self.stdout.write(
                f"Updating index \"{index_key}\" with kwargs {index.get('kwargs', {})}"
            )
            for source_name, source_cls in source_pool.get_sources().items():
                source = source_cls(**index.get("kwargs", {}))
                self.stdout.write(
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
                delete_result = (
                    IndexEntry.objects.filter(
                        index_key=index_key,
                        content_type=content_type,
                    )
                    .exclude(
                        object_id__in=current_ids,
                    )
                    .delete()
                )
                self.stdout.write(f"> Done. Removed from index: {delete_result[0]}")
