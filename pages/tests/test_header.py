from django.urls import reverse

from accounts.factories import UserFactory
from companies.factories import CompanyFactory
from companies.models import CompanyOwner
from utils.testcases import BaseTestCase


class TestHeader(BaseTestCase):
    def setUp(self):
        self.login_text = "Log in"
        self.sign_up_text = "Sign up"
        self.logout_text = "Log out"
        # Create required models
        self.company = CompanyFactory()
        self.user = UserFactory(company=self.company)
        self.other_user = UserFactory(company=self.company)
        self.different_company_user = UserFactory()

        # Make first user the company owner
        CompanyOwner.objects.create(company=self.company, owner=self.user)

        self.client.force_login(user=self.user)

    def test_header_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("home"), follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.login_text)
        self.assertContains(response, self.sign_up_text)

        self.assertNotContains(response, "Settings")

    def test_header_logged_in_admin(self):
        response = self.client.get(reverse("home"), follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, self.login_text)
        self.assertNotContains(response, self.sign_up_text)

        self.assertContains(response, self.logout_text)
        self.assertContains(response, "Settings")
        self.assertContains(response, "Home")

    def test_header_logged_in_none_admin(self):
        self.client.force_login(user=self.other_user)
        response = self.client.get(reverse("home"), follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, self.login_text)
        self.assertNotContains(response, self.sign_up_text)
        self.assertNotContains(response, "Settings")

        self.assertContains(response, "Home")
        self.assertContains(response, self.logout_text)

    def test_header_logged_in_other_company(self):
        self.client.force_login(user=self.different_company_user)
        response = self.client.get(reverse("home"), follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Home")
        self.assertContains(response, self.logout_text)

        self.assertNotContains(response, self.login_text)
        self.assertNotContains(response, self.sign_up_text)
        self.assertNotContains(response, "Settings")
