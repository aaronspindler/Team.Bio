from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from companies.factories import CompanyFactory
from companies.models import CompanyOwner


class TestHeader(TestCase):
    def setUp(self):
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
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Log In')
        self.assertContains(response, 'Sign Up')

        self.assertNotContains(response, 'Company Admin')

    def test_header_logged_in_admin(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, 'Log In')
        self.assertNotContains(response, 'Sign Up')

        self.assertContains(response, 'Logout')
        self.assertContains(response, 'Company Admin')
        self.assertContains(response, 'Home')

    def test_header_logged_in_none_admin(self):
        self.client.force_login(user=self.other_user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, 'Log In')
        self.assertNotContains(response, 'Sign Up')
        self.assertNotContains(response, 'Company Admin')

        self.assertContains(response, 'Home')
        self.assertContains(response, 'Logout')

    def test_header_logged_in_other_company(self):
        self.client.force_login(user=self.different_company_user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Home')
        self.assertContains(response, 'Logout')

        self.assertNotContains(response, 'Log In')
        self.assertNotContains(response, 'Sign Up')
        self.assertNotContains(response, 'Company Admin')
