from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Try send something to Sentry!"

    def handle(self, *args, **options):
        pass
