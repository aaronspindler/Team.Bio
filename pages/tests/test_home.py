from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from companies.factories import CompanyFactory
from companies.models import CompanyOwner


class TestHome(TestCase):
    def setUp(self):
        # Create required models
        self.company = CompanyFactory()
        self.user = UserFactory(company=self.company)
        self.other_user = UserFactory(company=None)
        self.different_company_user = UserFactory()

        # Make first user the company owner
        CompanyOwner.objects.create(company=self.company, owner=self.user)

        self.client.force_login(user=self.user)

    def test_logged_in_is_member(self):
        response = self.client.get(reverse("home"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/home.html")

    def test_logged_in_is_not_member(self):
        self.client.force_login(user=self.other_user)
        response = self.client.get(reverse("home"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("home"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")
