from django.test import TestCase

from accounts.factories import UserFactory
from companies.factories import CompanyFactory
from companies.models import CompanyOwner


class TestModels(TestCase):
    def setUp(self):
        self.company = CompanyFactory()
        self.user = UserFactory(company=self.company)

    def test_overridden_save(self):
        user = UserFactory(email="Aaron@Spindlers.ca")
        self.assertEqual(user.email_root, "spindlers.ca")
        self.assertEqual(user.email_prefix, "aaron")

    def test_user_member_of_company_member(self):
        expected_result = True
        actual_result = self.user.is_member_of_company
        self.assertEqual(expected_result, actual_result)

    def test_user_member_of_company_owner(self):
        CompanyOwner.objects.create(company=self.company, owner=self.user)
        expected_result = True
        actual_result = self.user.is_member_of_company
        self.assertEqual(expected_result, actual_result)

    def test_user_member_of_company_no_member_or_owner(self):
        self.user.company = None
        self.user.save()
        expected_result = False
        actual_result = self.user.is_member_of_company
        self.assertEqual(expected_result, actual_result)

    def test_user_email_root(self):
        user = UserFactory(email="aaron@spindlers.ca")
        self.assertEqual(user.email_root, "spindlers.ca")

    def test_user_email_prefix(self):
        user = UserFactory(email="aaron@spindlers.ca")
        self.assertEqual(user.email_prefix, "aaron")

    def test_user_address_string(self):
        user = UserFactory(address_1="123 Main St")
        self.assertEqual(user.address_string, "123 Main St")

        user = UserFactory(address_1=" 123 Main St   ", city="   Toronto ")
        self.assertEqual(user.address_string, "123 Main St Toronto")

        user = UserFactory(
            address_1=" 123 Main St   ", city="   Toronto ", prov_state="   ON "
        )
        self.assertEqual(user.address_string, "123 Main St Toronto ON")

        user = UserFactory(
            address_1=" 123 Main St   ",
            city="   Toronto ",
            prov_state="   ON ",
            country="   Canada ",
        )
        self.assertEqual(user.address_string, "123 Main St Toronto ON Canada")

        user = UserFactory(
            address_1=" 123 Main St   ",
            city="   Toronto ",
            prov_state="   ON ",
            country="   Canada ",
            postal_code="   M1M 1M1 ",
        )
        self.assertEqual(user.address_string, "123 Main St Toronto ON Canada M1M 1M1")

    def test_user_geo_code_address(self):
        user = UserFactory(address_1="123 Main St", city="Toronto", country="Canada")
        lat, lng, place_id = user.geo_code_address()
        self.assertEqual(lat, 43.6826959)
        self.assertEqual(lng, -79.2994168)
        self.assertEqual(place_id, "ChIJP_BKRhrM1IkRuTDbHDrQNhw")
