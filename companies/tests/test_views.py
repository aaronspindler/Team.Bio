from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from companies.factories import CompanyFactory
from companies.models import CompanyOwner, Company


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

    def test_company_admin(self):
        response = self.client.get(reverse('company_admin'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/company_admin.html")
        self.assertTemplateNotUsed(response, "account/login.html")

    def test_company_home(self):
        response = self.client.get(reverse('company_home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/home.html")
        self.assertTemplateNotUsed(response, "account/login.html")

    def test_login_required_create_company(self):
        self.client.logout()
        response = self.client.get(reverse('create_company'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "companies/create_company.html")
        self.assertTemplateUsed(response, "account/login.html")

    def test_create_company_already_have_company(self):
        response = self.client.get(reverse('create_company'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "companies/create_company.html")
        self.assertTemplateUsed(response, "companies/home.html")

    def test_create_company_no_company(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse('create_company'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/create_company.html")

    def test_create_company_post_valid(self):
        self.client.force_login(self.other_user)
        self.assertIsNone(self.other_user.company)
        pre_company_count = Company.objects.count()
        pre_company_owner_count = CompanyOwner.objects.count()
        data = {
            'name': 'Freedom Health',
            'url': 'https://www.freedomhealth.com'
        }
        response = self.client.post(reverse('create_company'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/home.html")
        self.assertContains(response, 'Freedom Health')
        self.assertGreater(Company.objects.count(), pre_company_count)
        self.assertGreater(CompanyOwner.objects.count(), pre_company_owner_count)
        self.other_user.refresh_from_db()
        self.assertIsNotNone(self.other_user.company)

    def test_create_company_post_already_have_company(self):
        # Should not create a new company since the user is already a company owner
        data = {
            'name': 'Freedom Health',
            'url': 'https://www.freedomhealth.com'
        }
        pre_company_count = Company.objects.count()
        pre_company_owner_count = CompanyOwner.objects.count()
        response = self.client.post(reverse('create_company'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "companies/create_company.html")
        self.assertTemplateUsed(response, "companies/home.html")
        self.assertNotContains(response, 'Freedom Health')
        self.assertEqual(Company.objects.count(), pre_company_count)
        self.assertEqual(CompanyOwner.objects.count(), pre_company_owner_count)

    def test_create_company_post_invalid(self):
        self.client.force_login(self.other_user)
        pre_company_count = Company.objects.count()
        pre_company_owner_count = CompanyOwner.objects.count()
        # Missing company name
        data = {
            'url': 'https://www.freedomhealth.com'
        }
        response = self.client.post(reverse('create_company'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/create_company.html")
        self.assertContains(response, 'https://www.freedomhealth.com')
        self.assertEqual(Company.objects.count(), pre_company_count)
        self.assertEqual(CompanyOwner.objects.count(), pre_company_owner_count)
