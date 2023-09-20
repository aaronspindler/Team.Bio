from django.conf import settings

from accounts.factories import UserFactory
from accounts.models import User
from accounts.utils import (
    attempt_connect_user_to_a_company,
    attempt_connect_user_with_invites,
    merge_user,
)
from companies.factories import CompanyFactory, InviteFactory
from companies.models import Invite
from utils.testcases import BaseTestCase


class TestUtils(BaseTestCase):
    def setUp(self):
        self.company = CompanyFactory(url="https://www.spindlers.ca")
        self.user = UserFactory(company=None, email="aaron@spindlers.ca")

    def test_attempt_connect_user_to_a_company_success(self):
        self.assertIsNone(self.user.company)
        self.assertTrue(attempt_connect_user_to_a_company(self.user.pk))
        self.user.refresh_from_db()
        self.assertEqual(self.user.company, self.company)

    def test_attempt_connect_user_to_a_company_already_in_company(self):
        self.user = UserFactory(company=self.company)
        self.assertFalse(attempt_connect_user_to_a_company(self.user.pk))

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

    def test_merge_user(self):
        company = CompanyFactory()
        pre_user_count = User.objects.count()
        initial_user = UserFactory(company=company, email="asdf@asdf.com")
        initial_user_data = {
            "short_bio": initial_user.short_bio,
            "title": initial_user.title,
            "linkedin": initial_user.linkedin,
            "twitter": initial_user.twitter,
            "github": initial_user.github,
        }
        new_user = UserFactory(email=initial_user.email, company=None)
        self.assertEqual(User.objects.count(), pre_user_count + 2)  # Should be 2 new users
        self.assertNotEqual(initial_user.pk, new_user.pk)  # pks for the new users should not be the same
        self.assertNotEqual(initial_user.company, new_user.company)  # They should not be in the same company
        self.assertEqual(initial_user.email, new_user.email)  # They should have the same email

        self.assertNotEqual(initial_user.short_bio, new_user.short_bio)
        self.assertNotEqual(initial_user.title, new_user.title)
        self.assertNotEqual(initial_user.linkedin, new_user.linkedin)
        self.assertNotEqual(initial_user.twitter, new_user.twitter)
        self.assertNotEqual(initial_user.github, new_user.github)

        merge_user(new_user.pk)

        self.assertEqual(User.objects.count(), pre_user_count + 1)

        new_user.refresh_from_db()
        self.assertEqual(new_user.short_bio, initial_user_data["short_bio"])
        self.assertEqual(new_user.title, initial_user_data["title"])
        self.assertEqual(new_user.linkedin, initial_user_data["linkedin"])
        self.assertEqual(new_user.twitter, initial_user_data["twitter"])
        self.assertEqual(new_user.github, initial_user_data["github"])

        self.assertEqual(new_user.company, company)
