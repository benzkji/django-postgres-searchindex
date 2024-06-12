from django.core.management import BaseCommand

from postgres_searchindex.management.indexing import update_indexes


class Command(BaseCommand):
    help = "update index"

    def handle(self, *args, **options):
        update_indexes()
