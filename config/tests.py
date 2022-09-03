from django.test import TestCase
from django.urls import reverse


class TestConfigView(TestCase):
    def test_health_view(self):
        response = self.client.get(reverse('system_health'))
        self.assertEqual(response.status_code, 200)
