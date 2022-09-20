from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from accounts.models import CustomUser
from companies.factories import CompanyFactory
from companies.models import CompanyOwner, Company


class TestCompanyViews(TestCase):
    def setUp(self):
        # Create required models
        self.company = CompanyFactory()
        self.user = UserFactory(company=self.company)
        self.company_user = UserFactory(company=self.company)
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

    def test_login_required_company_settings(self):
        self.client.logout()
        response = self.client.get(reverse('company_settings'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "companies/company_settings.html")
        self.assertTemplateUsed(response, "account/login.html")

    def test_company_settings_is_admin(self):
        response = self.client.get(reverse('company_settings'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/company_settings.html")
        self.assertTemplateNotUsed(response, "account/login.html")

    def test_company_settings_is_not_admin(self):
        """
        If the user is not an owner/admin of the company, they should be redirected to a 404 page
        """
        self.client.force_login(user=self.company_user)
        response = self.client.get(reverse('company_settings'), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_company_home(self):
        response = self.client.get(reverse('company_home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/home.html")
        self.assertTemplateNotUsed(response, "account/login.html")

    def test_company_home_no_company(self):
        self.client.force_login(self.other_user)
        response = self.client.get(reverse('company_home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/create_company.html")
        self.assertTemplateNotUsed(response, "companies/home.html")

    def test_company_home_company_exists_for_user(self):
        user = UserFactory(email='aaron@spindlers.ca', company=None)
        company = CompanyFactory(url='https://www.spindlers.ca')
        self.client.force_login(user)
        response = self.client.get(reverse('company_home'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "companies/create_company.html")
        self.assertTemplateUsed(response, "companies/home.html")

        user.refresh_from_db()
        self.assertEqual(user.company, company)

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

    def test_remove_user_login_required_post(self):
        self.client.logout()
        response = self.client.post(reverse('remove_user', kwargs={'user_to_remove_pk': self.company_user.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "companies/remove_user.html")
        self.assertTemplateUsed(response, "account/login.html")

    def test_remove_user_login_required_get(self):
        self.client.logout()
        response = self.client.get(reverse('remove_user', kwargs={'user_to_remove_pk': self.company_user.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "companies/remove_user.html")
        self.assertTemplateUsed(response, "account/login.html")

    def test_remove_user_is_company_owner_post(self):
        self.client.force_login(self.company_user)
        response = self.client.post(reverse('remove_user', kwargs={'user_to_remove_pk': self.company_user.pk}), follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, "companies/remove_user.html")
        self.assertTemplateUsed(response, "404.html")

    def test_remove_user_is_company_owner_get(self):
        self.client.force_login(self.company_user)
        response = self.client.get(reverse('remove_user', kwargs={'user_to_remove_pk': self.company_user.pk}), follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, "companies/remove_user.html")
        self.assertTemplateUsed(response, "404.html")

    def test_remove_user_is_a_company_owner(self):
        # GET
        self.assertFalse(CustomUser.objects.filter(is_active=False).exists())
        response = self.client.get(reverse('remove_user', kwargs={'user_to_remove_pk': self.user.pk}), follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, "companies/remove_user.html")
        self.assertTemplateUsed(response, "404.html")
        self.assertFalse(CustomUser.objects.filter(is_active=False).exists())

        # POST
        self.assertFalse(CustomUser.objects.filter(is_active=False).exists())
        response = self.client.post(reverse('remove_user', kwargs={'user_to_remove_pk': self.user.pk}), follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, "companies/remove_user.html")
        self.assertTemplateUsed(response, "404.html")
        self.assertFalse(CustomUser.objects.filter(is_active=False).exists())

    def test_remove_user_not_in_company(self):
        # GET
        self.assertFalse(CustomUser.objects.filter(is_active=False).exists())
        response = self.client.get(reverse('remove_user', kwargs={'user_to_remove_pk': self.different_company_user.pk}), follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, "companies/remove_user.html")
        self.assertTemplateUsed(response, "404.html")
        self.assertFalse(CustomUser.objects.filter(is_active=False).exists())

        # POST
        self.assertFalse(CustomUser.objects.filter(is_active=False).exists())
        response = self.client.post(reverse('remove_user', kwargs={'user_to_remove_pk': self.different_company_user.pk}), follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, "companies/remove_user.html")
        self.assertTemplateUsed(response, "404.html")
        self.assertFalse(CustomUser.objects.filter(is_active=False).exists())

    def test_remove_user_get(self):
        response = self.client.get(reverse('remove_user', kwargs={'user_to_remove_pk': self.company_user.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/remove_user.html")
        self.assertFalse(CustomUser.objects.filter(is_active=False).exists())

    def test_remove_user_post(self):
        self.assertFalse(CustomUser.objects.filter(is_active=False).exists())
        response = self.client.post(reverse('remove_user', kwargs={'user_to_remove_pk': self.company_user.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/company_settings.html")
        self.assertTrue(CustomUser.objects.filter(is_active=False).exists())
