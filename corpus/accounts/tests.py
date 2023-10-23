from accounts.models import User
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse


class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(
            first_name="Test",
            last_name="User",
            email="testuser@gmail.com",
            phone_no="9876543210",
            gender="M",
            password="testuser@password",
        )
        self.signin_path = reverse("accounts_signin")
        self.signup_path = reverse("accounts_signup")
        self.signout_path = reverse("accounts_signout")
        self.index_path = reverse("index")

    def test_successful_signup(self):
        form_data = {
            "first_name": "First 1",
            "last_name": "Last 1",
            "email": "user1@gmail.com",
            "phone_no": "0000000000",
            "gender": "M",
            "password1": "user1@password",
            "password2": "user1@password",
        }

        response = self.client.post(self.signup_path, form_data, follow=True)
        messages = list(response.context.get("messages"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "You have been successfully registered. Please sign in!"
        )

        self.assertRedirects(response, self.signin_path)

    def test_unsuccessful_signup(self):
        form_data = {
            "first_name": "First 1",
            "last_name": "Last 1",
            "email": "testuser@gmail.com",
            "phone_no": "0000000000",
            "gender": "M",
            "password1": "user1@password",
            "password2": "user1@password",
        }

        response = self.client.post(self.signup_path, form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context.get("form").errors)

    def test_successful_signin(self):
        form_data = {
            "username": "testuser@gmail.com",
            "password": "testuser@password",
        }

        response = self.client.post(self.signin_path, form_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_unsuccessful_signin(self):
        form_data = {
            "username": "testuser@gmail.com",
            "password": "testuser",
        }

        response = self.client.post(self.signin_path, form_data, follow=True)
        form_errors = response.context.get("form").errors

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(form_errors)
