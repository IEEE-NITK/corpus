from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="newsletter_home"),
    path(
        "announcements/manage",
        views.manage_announcements,
        name="newsletter_manage_announcements",
    ),
    path(
        "announcements/new", views.new_announcement, name="newsletter_new_announcement"
    ),
    path(
        "announcements/edit/<int:pk>",
        views.edit_announcement,
        name="newsletter_edit_announcement",
    ),
    path(
        "announcement/toggle/<int:pk>",
        views.toggle_announcement,
        name="newsletter_toggle_announcement",
    ),
    path(
        "announcement/delete/<int:pk>",
        views.delete_announcement,
        name="newsletter_delete_announcement",
    ),
    path("calendar/", views.calendar_view, name="newsletter_calendar"),
    path(
        "archive/<int:pk>/", 
        views.archived_event_detail, 
        name="newsletter_archived_event_detail"
    ),
    path("archive/", views.archived_events_view, name="newsletter_archived_events"),  
]
