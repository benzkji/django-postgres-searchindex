# commands/reindex_indexes.py
from django.core.management import BaseCommand
from ._utils import delete_indexes, update_indexes

class Command(BaseCommand):
    help = "Reindexing postgres "

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reindex without confirmation'
        )

    def handle(self, *args, **options):
        if not options['force']:
            self.stdout.write(self.style.WARNING(
                "This will delete all indexes and reindex them."
                " Are you sure you want to proceed?"
            ))

            confirmation = input("Type 'yes' to continue: ")

            if confirmation.lower() != 'yes':
                self.stdout.write(self.style.ERROR("Reindexing aborted."))
                return

        self.stdout.write(self.style.SUCCESS("Starting the reindexing process..."))
        delete_indexes()
        update_indexes()
        self.stdout.write(self.style.SUCCESS("Reindexing completed successfully!"))
