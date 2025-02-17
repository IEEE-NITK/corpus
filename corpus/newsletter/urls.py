from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="newsletter_home"),
    path("manage_announcements/", views.manage_announcements, name="newsletter_manage_announcements"),
    path("new_announcement/", views.new_announcement, name="newsletter_new_announcement"),
    path("edit_announcement/<int:pk>", views.edit_announcement, name="newsletter_edit_announcement"),
    path("toggle_announcement/<int:pk>", views.toggle_announcement, name="newsletter_toggle_announcement"),
    path("delete_announcement/<int:pk>", views.delete_announcement, name="newsletter_delete_announcement")
]