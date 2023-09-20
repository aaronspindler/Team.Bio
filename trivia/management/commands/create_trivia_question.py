from django.core.management.base import BaseCommand

from trivia.tasks import create_trivia_question


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_trivia_question()
