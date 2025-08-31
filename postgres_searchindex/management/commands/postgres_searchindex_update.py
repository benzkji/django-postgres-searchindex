from django.core.management import BaseCommand

from postgres_searchindex.management.indexing import update_index


class Command(BaseCommand):
    help = "update index"

    def handle(self, *args, **options):
        update_index(self.stdout)
