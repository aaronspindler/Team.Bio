from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction


class Command(BaseCommand):
    help = 'Loads initial data from fixtures'

    def handle(self, *args, **options):
        with transaction.atomic():
            call_command('loaddata', 'data.json')
