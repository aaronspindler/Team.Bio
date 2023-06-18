from django.core.management.base import BaseCommand

from utils.ai import trivia_question


class Command(BaseCommand):
    def handle(self, *args, **options):
        trivia_question()
