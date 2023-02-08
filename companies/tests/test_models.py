from decimal import Decimal

from django.test import TestCase

from accounts.factories import UserFactory
from companies.factories import CompanyFactory
from companies.models import CompanyOwner


class TestModels(TestCase):
    def setUp(self):
        self.company = CompanyFactory()
        self.user = UserFactory(company=self.company)
        self.user2 = UserFactory(company=self.company)
        self.company_owner = CompanyOwner.objects.create(
            company=self.company, owner=self.user
        )

    def test_company_get_owners_single(self):
        expected_result = [self.user]
        actual_result = self.company.get_owners
        self.assertEqual(expected_result, actual_result)

    def test_company_get_owners_multiple(self):
        CompanyOwner.objects.create(company=self.company, owner=self.user2)
        expected_result = [self.user, self.user2]
        actual_result = self.company.get_owners
        self.assertEqual(expected_result, actual_result)

    def test_company_str(self):
        self.assertEqual(str(self.company), self.company.name)

    def test_company_owner_str(self):
        self.assertEqual(
            str(self.company_owner), f"{self.company} {self.company_owner.owner}"
        )

    def test_company_save_url_root(self):
        company = CompanyFactory(url="https://www.spindlers.ca")
        self.assertEqual(company.url_root, "spindlers.ca")

    def test_calculate_geo_midpoint(self):
        result = self.company.calculate_geo_midpoint()
        self.assertEqual(result, (0.0, 0.0))

        UserFactory(
            address_1="123 Main St",
            city="Toronto",
            country="Canada",
            company=self.company,
        )
        UserFactory(
            address_1="123 Main St",
            city="Edmonton",
            country="Canada",
            company=self.company,
        )

        result = self.company.calculate_geo_midpoint()
        self.assertEqual(result, (Decimal("48.6143971"), Decimal("-96.3965717")))
