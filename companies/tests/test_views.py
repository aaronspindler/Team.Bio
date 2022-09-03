from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from companies.factories import CompanyFactory
from companies.models import CompanyOwner


class TestCompanyViews(TestCase):
    def setUp(self):
        # Create required models
        self.company = CompanyFactory()
        self.user = UserFactory(company=self.company)
        self.other_user = UserFactory(company=None)
        self.different_company_user = UserFactory()

        # Make first user the company owner
        CompanyOwner.objects.create(company=self.company, owner=self.user)

        self.client.force_login(user=self.user)

    # Confirm that login required are working for all URLs
    def test_login_required_home(self):
        self.client.logout()
        response = self.client.get(reverse('company_home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "companies/home.html")
        self.assertTemplateUsed(response, "account/login.html")

    def test_login_required_company_admin(self):
        self.client.logout()
        response = self.client.get(reverse('company_admin'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "companies/company_admin.html")
        self.assertTemplateUsed(response, "account/login.html")

    def test_login_required_create_company(self):
        self.client.logout()
        response = self.client.get(reverse('create_company'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "companies/company_create.html")
        self.assertTemplateUsed(response, "account/login.html")
