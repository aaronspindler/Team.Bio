from django.conf import settings
from django.test import TestCase

from accounts.factories import UserFactory
from accounts.utils import attempt_connect_user_to_a_company
from companies.factories import CompanyFactory


class TestUtils(TestCase):
    def setUp(self):
        self.company = CompanyFactory(url='https://www.spindlers.ca')
        self.user = UserFactory(company=None, email='aaron@spindlers.ca')

    def test_attempt_connect_user_to_a_company_success(self):
        self.assertIsNone(self.user.company)
        self.assertTrue(attempt_connect_user_to_a_company(self.user))
        self.user.refresh_from_db()
        self.assertEqual(self.user.company, self.company)

    def test_attempt_connect_user_to_a_company_no_company(self):
        self.user = UserFactory(company=None, email='fred@flintstone.com')
        self.assertIsNone(self.user.company)
        self.assertFalse(attempt_connect_user_to_a_company(self.user))

    def test_attempt_connect_user_to_blacklisted_domain_root(self):
        for domain in settings.BLACKLISTED_DOMAIN_ROOTS:
            CompanyFactory(url=f'https://www.{domain}')
            user = UserFactory(company=None, email=f'aaron@{domain}')
            self.assertFalse(attempt_connect_user_to_a_company(user))
