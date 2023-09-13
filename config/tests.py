from django.urls import reverse

from utils.testcases import BaseTestCase


class TestConfigView(BaseTestCase):
    def test_health_view(self):
        response = self.client.get(reverse("system_health"))
        self.assertEqual(response.status_code, 200)
