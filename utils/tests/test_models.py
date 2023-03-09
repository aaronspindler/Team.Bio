from django.test import TestCase

from utils.models import Email


class TestModels(TestCase):
    def test_email(self):
        email = Email.objects.create()
        print(email)
