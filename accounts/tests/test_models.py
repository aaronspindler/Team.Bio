from django.test import TestCase

from accounts.factories import UserFactory
from companies.factories import CompanyFactory
from companies.models import CompanyOwner


class TestModels(TestCase):
    def setUp(self):
        self.company = CompanyFactory()
        self.user = UserFactory(company=self.company)

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
