from django.test import TestCase

from accounts.factories import UserFactory
from companies.factories import CompanyFactory


class TestActivity(TestCase):
    def setUp(self):
        # Create required models
        self.company = CompanyFactory()
        self.user = UserFactory()
