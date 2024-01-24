from django.test import SimpleTestCase
from django.urls import resolve
from django.urls import reverse
from robotrix.views import add_member
from robotrix.views import admin
from robotrix.views import announcements_management
from robotrix.views import create_team
from robotrix.views import delete_announcement
from robotrix.views import delete_payment_proof
from robotrix.views import home
from robotrix.views import index
from robotrix.views import mark_payment_complete
from robotrix.views import mark_payment_incomplete
from robotrix.views import register
from robotrix.views import team_management
from robotrix.views import team_page
from robotrix.views import upload_payment_proof
from robotrix.views import user_management


class UrlsTestCase(SimpleTestCase):
    def test_home_url_is_resolved(self):
        url = reverse("robotrix_home")
        self.assertEquals(resolve(url).func, home)

    def test_index_url_is_resolved(self):
        url = reverse("robotrix_index")
        self.assertEquals(resolve(url).func, index)

    def test_register_url_is_resolved(self):
        url = reverse("robotrix_register")
        self.assertEquals(resolve(url).func, register)

    def test_create_team_url_is_resolved(self):
        url = reverse("robotrix_create_team")
        self.assertEquals(resolve(url).func, create_team)

    def test_add_member_url_is_resolved(self):
        url = reverse("robotrix_add_member2")
        self.assertEquals(resolve(url).func, add_member)

    def test_upload_payment_proof_url_is_resolved(self):
        url = reverse("robotrix_upload_payment_proof")
        self.assertEquals(resolve(url).func, upload_payment_proof)

    def test_delete_payment_proof_url_is_resolved(self):
        url = reverse("robotrix_delete_payment_proof")
        self.assertEquals(resolve(url).func, delete_payment_proof)

    def test_admin_url_is_resolved(self):
        url = reverse("robotrix_admin")
        self.assertEquals(resolve(url).func, admin)

    def test_team_management_url_is_resolved(self):
        url = reverse("robotrix_admin_teams")
        self.assertEquals(resolve(url).func, team_management)

    def test_team_page_url_is_resolved(self):
        url = reverse("robotrix_admin_team_page", args=[1])
        self.assertEquals(resolve(url).func, team_page)

    def test_user_management_url_is_resolved(self):
        url = reverse("robotrix_admin_users")
        self.assertEquals(resolve(url).func, user_management)

    def test_announcements_management_url_is_resolved(self):
        url = reverse("robotrix_announcements")
        self.assertEquals(resolve(url).func, announcements_management)

    def test_delete_announcement_url_is_resolved(self):
        url = reverse("robotrix_delete_announcement", args=[1])
        self.assertEquals(resolve(url).func, delete_announcement)

    def test_mark_payment_complete_url_is_resolved(self):
        url = reverse("robotrix_admin_mark_payment_complete", args=[1])
        self.assertEquals(resolve(url).func, mark_payment_complete)

    def test_mark_payment_incomplete_url_is_resolved(self):
        url = reverse("robotrix_admin_mark_payment_incomplete", args=[1])
        self.assertEquals(resolve(url).func, mark_payment_incomplete)
