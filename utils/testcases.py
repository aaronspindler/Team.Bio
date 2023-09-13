from django.contrib.sites.models import Site
from django.test import TestCase


class BaseTestCase(TestCase):
    databases = "__all__"

    def setUp(self):
        super().setUp()
        self.site = Site.objects.create(domain="testserver", name="testserver")
