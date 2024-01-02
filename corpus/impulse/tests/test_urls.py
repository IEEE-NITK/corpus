from django.test import SimpleTestCase
from django.urls import reverse, resolve

from impulse.views import home, index, register, create_team, add_member, upload_payment_proof, delete_payment_proof
from impulse.views import admin, team_management, team_page, user_management, announcements_management, delete_announcement, mark_payment_complete, mark_payment_incomplete


class UrlsTestCase(SimpleTestCase):
    def test_home_url_is_resolved(self):
        url = reverse('impulse_home')
        self.assertEquals(resolve(url).func, home)

    def test_index_url_is_resolved(self):
        url = reverse('impulse_index')
        self.assertEquals(resolve(url).func, index)

    def test_register_url_is_resolved(self):
        url = reverse('impulse_register')
        self.assertEquals(resolve(url).func, register)
    
    def test_create_team_url_is_resolved(self):
        url = reverse('impulse_create_team')
        self.assertEquals(resolve(url).func, create_team)

    def test_add_member_url_is_resolved(self):
        url = reverse('impulse_add_member2')
        self.assertEquals(resolve(url).func, add_member)

    def test_upload_payment_proof_url_is_resolved(self):
        url = reverse('impulse_upload_payment_proof')
        self.assertEquals(resolve(url).func, upload_payment_proof)

    def test_delete_payment_proof_url_is_resolved(self):
        url = reverse('impulse_delete_payment_proof')
        self.assertEquals(resolve(url).func, delete_payment_proof)

    def test_admin_url_is_resolved(self):
        url = reverse('impulse_admin')
        self.assertEquals(resolve(url).func, admin)

    def test_team_management_url_is_resolved(self):
        url = reverse('impulse_admin_teams')
        self.assertEquals(resolve(url).func, team_management)

    def test_team_page_url_is_resolved(self):
        url = reverse('impulse_admin_team_page', args=[1])
        self.assertEquals(resolve(url).func, team_page)

    def test_user_management_url_is_resolved(self):
        url = reverse('impulse_admin_users')
        self.assertEquals(resolve(url).func, user_management)

    def test_announcements_management_url_is_resolved(self):
        url = reverse('impulse_announcements')
        self.assertEquals(resolve(url).func, announcements_management)

    def test_delete_announcement_url_is_resolved(self):
        url = reverse('impulse_delete_announcement', args=[1])
        self.assertEquals(resolve(url).func, delete_announcement)

    def test_mark_payment_complete_url_is_resolved(self):
        url = reverse('impulse_admin_mark_payment_complete', args=[1])
        self.assertEquals(resolve(url).func, mark_payment_complete)

    def test_mark_payment_incomplete_url_is_resolved(self):
        url = reverse('impulse_admin_mark_payment_incomplete', args=[1])
        self.assertEquals(resolve(url).func, mark_payment_incomplete)

        