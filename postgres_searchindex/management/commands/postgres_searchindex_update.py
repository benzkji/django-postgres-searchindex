from django.core.management import BaseCommand

from ._utils import update_indexes


class Command(BaseCommand):
    help = "Update/build index"

    def handle(self, *args, **options):
        update_indexes()
