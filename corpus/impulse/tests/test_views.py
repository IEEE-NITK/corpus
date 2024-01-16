from django.test import Client
from django.test import TestCase
from django.urls import reverse


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_GET(self):
        response = self.client.get(reverse("impulse_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "impulse/home.html")
