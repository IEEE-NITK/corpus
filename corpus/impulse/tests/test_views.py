from django.test import Client
from django.test import TestCase
from django.urls import reverse
from impulse.models import Announcement
from impulse.models import ImpulseUser
from impulse.models import Team


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_GET(self):
        response = self.client.get(reverse("impulse_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "impulse/home.html")
