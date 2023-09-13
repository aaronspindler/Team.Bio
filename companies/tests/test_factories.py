from companies.factories import CompanyFactory
from companies.models import Company
from utils.testcases import BaseTestCase


class TestFactories(BaseTestCase):
    def test_company_factory(self):
        """
        Company Factory
        """
        pre_count = Company.objects.count()
        factory = CompanyFactory()
        post_count = Company.objects.count()
        self.assertGreater(post_count, pre_count)
        self.assertIsNotNone(factory.name)
        self.assertIsNotNone(factory.url)

    def test_multiple_company_creation(self):
        """
        Multiple Company Creation
        """
        company = CompanyFactory()
        company2 = CompanyFactory()

        self.assertNotEqual(company.name, company2.name)
