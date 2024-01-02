from django.test import TestCase, Client
from django.urls import reverse
from impulse.models import ImpulseUser, Team, Announcement

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_GET(self):
        response = self.client.get(reverse("impulse_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "impulse/home.html")
