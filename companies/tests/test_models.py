from django.test import TestCase

from accounts.factories import UserFactory
from companies.factories import CompanyFactory
from companies.models import CompanyOwner


class TestModels(TestCase):
    def setUp(self):
        self.company = CompanyFactory()
        self.user = UserFactory(company=self.company)
        self.user2 = UserFactory(company=self.company)
        CompanyOwner.objects.create(company=self.company, owner=self.user)

    def test_company_get_owners_single(self):
        expected_result = [self.user]
        actual_result = self.company.get_owners()
        self.assertEqual(expected_result, actual_result)

    def test_company_get_owners_multiple(self):
        CompanyOwner.objects.create(company=self.company, owner=self.user2)
        expected_result = [self.user, self.user2]
        actual_result = self.company.get_owners()
        self.assertEqual(expected_result, actual_result)
