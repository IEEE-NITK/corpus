from accounts.models import User
from accounts.models import ExecutiveMember
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from config.models import SIG


class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
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

    def test_signout(self):
        self.client.login(username="testuser@gmail.com", password="testuser@password")
        response = self.client.get(self.signout_path, follow=True)
        messages = list(response.context.get("messages"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(messages[0]), "Successfully signed out.")
        self.assertRedirects(response, self.index_path)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_profile_view(self):

        sigTemp = SIG.objects.create(name="Compsoc")

        exec_member = ExecutiveMember.objects.create(
            user=self.user,
            roll_number="000IT456",
            edu_email="test@nitk.edu.in",
            reg_number="123456",
            sig=sigTemp,
            minor_branch="SM",
            ieee_number="123",
            ieee_email="test@ieee.org",
            linkedin="https://linkedin.com/in/testuser",
            github="https://github.com/testuser",
            is_nep=False,
            hide_github=False,
            hide_linkedin=False,
        )

        profile_path = reverse("accounts_profile", args=[exec_member.roll_number])
        response = self.client.get(profile_path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
        self.assertIn("exec_member", response.context)
        self.assertIn("profile_user", response.context)
        self.assertEqual(response.context["exec_member"].roll_number, "000IT456")

    def test_edit_profile_user_not_loggedIn(self):
        sigTemp = SIG.objects.create(name="Compsoc")

        exec_member = ExecutiveMember.objects.create(
            user=self.user,
            roll_number="000IT456",
            edu_email="test@nitk.edu.in",
            reg_number="123456",
            sig=sigTemp,
            minor_branch="SM",
            ieee_number="123",
            ieee_email="test@ieee.org",
            linkedin="https://linkedin.com/in/testuser",
            github="https://github.com/testuser",
            is_nep=False,
            hide_github=False,
            hide_linkedin=False,
        )

        edit_path = reverse("edit_profile", args=[exec_member.roll_number])
        response = self.client.get(edit_path,follow=True)

        self.assertRedirects(response, f"{reverse('accounts_signin')}?next={edit_path}")
    
    def test_edit_profile_user_loggedIn(self):
        sigTemp = SIG.objects.create(name="Compsoc")

        exec_member = ExecutiveMember.objects.create(
            user=self.user,
            roll_number="000IT456",
            edu_email="test@nitk.edu.in",
            reg_number="123456",
            sig=sigTemp,
            minor_branch="SM",
            ieee_number="123",
            ieee_email="test@ieee.org",
            linkedin="https://linkedin.com/in/testuser",
            github="https://github.com/testuser",
            is_nep=False,
            hide_github=False,
            hide_linkedin=False,
        )
    
        # self.client.login(username='testuser@gmail.com', password='testuser@password')
        self.assertTrue(self.client.login(username='testuser@gmail.com', password='testuser@password'))

        
        response = self.client.get(reverse('edit_profile',args=[exec_member.roll_number]))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'testuser@gmail.com')
        self.assertTemplateUsed(response,"accounts/edit_profile.html")
