from django.core.management.base import BaseCommand

from trivia.tasks import generate_trivia_question


class Command(BaseCommand):
    def handle(self, *args, **options):
        generate_trivia_question()
