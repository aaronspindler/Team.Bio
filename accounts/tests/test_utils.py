from django.conf import settings
from django.test import TestCase

from accounts.factories import UserFactory
from accounts.utils import (
    attempt_connect_user_to_a_company,
    attempt_connect_user_with_invites,
)
from companies.factories import CompanyFactory, InviteFactory
from companies.models import Invite


class TestUtils(TestCase):
    def setUp(self):
        self.company = CompanyFactory(url="https://www.spindlers.ca")
        self.user = UserFactory(company=None, email="aaron@spindlers.ca")

    def test_attempt_connect_user_to_a_company_success(self):
        self.assertIsNone(self.user.company)
        self.assertTrue(attempt_connect_user_to_a_company(self.user.pk))
        self.user.refresh_from_db()
        self.assertEqual(self.user.company, self.company)

    def test_attempt_connect_user_to_a_company_no_company(self):
        self.user = UserFactory(company=None, email="fred@flintstone.com")
        self.assertIsNone(self.user.company)
        self.assertFalse(attempt_connect_user_to_a_company(self.user.pk))

    def test_attempt_connect_user_to_blacklisted_domain_root(self):
        for domain in settings.BLACKLISTED_DOMAIN_ROOTS:
            CompanyFactory(url=f"https://www.{domain}")
            user = UserFactory(company=None, email=f"aaron@{domain}")
            self.assertFalse(attempt_connect_user_to_a_company(user.pk))

    def test_attempt_connect_user_with_invites_no_invite(self):
        self.assertIsNone(self.user.company)
        self.assertFalse(attempt_connect_user_with_invites(self.user.pk))

    def test_attempt_connect_user_with_invites_success(self):
        self.assertIsNone(self.user.company)
        InviteFactory(email=self.user.email, company=self.company)
        self.assertEqual(Invite.objects.count(), 1)
        self.assertTrue(attempt_connect_user_with_invites(self.user.pk))
        self.user.refresh_from_db()
        self.assertEqual(self.user.company, self.company)
        self.assertEqual(Invite.objects.count(), 0)

    def test_attempt_connect_user_with_invites_different_case(self):
        self.assertIsNone(self.user.company)
        self.user.email = self.user.email.upper()
        InviteFactory(email=self.user.email.lower(), company=self.company)
        self.assertEqual(Invite.objects.count(), 1)
        self.assertTrue(attempt_connect_user_with_invites(self.user.pk))
        self.user.refresh_from_db()
        self.assertEqual(self.user.company, self.company)
        self.assertEqual(Invite.objects.count(), 0)
