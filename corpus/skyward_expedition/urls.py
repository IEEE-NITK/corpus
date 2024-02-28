from django.urls import path
from skyward_expedition import views

urlpatterns = [
    path("", views.home, name="skyward_expedition_home"),
    path("register/", views.register, name="skyward_expedition_register"),
    path("dashboard/", views.dashboard, name="skyward_expedition_dashboard"),
    path("create_team/", views.create_team, name="skyward_expedition_create_team"),
    path(
        "create_invite/", views.create_invite, name="skyward_expedition_create_invite"
    ),
    path(
        "accept_invite/<int:pk>/",
        views.accept_invite,
        name="skyward_expedition_accept_invite",
    ),
    path(
        "delete_invite/<int:pk>/",
        views.delete_invite,
        name="skyward_expedition_delete_invite",
    ),
    path("admin/", views.admin, name="skyward_expedition_admin"),
    path(
        "admin/members/",
        views.member_dashboard,
        name="skyward_expedition_member_dashboard",
    ),
    path(
        "admin/teams/", views.teams_dashboard, name="skyward_expedition_teams_dashboard"
    ),
    path(
        "admin/teams/<int:team_id>",
        views.team_details,
        name="skyward_expedition_team_details",
    ),
    path(
        "admin/announcements",
        views.announcements_dashboard,
        name="skyward_expedition_announcements_dashboard",
    ),
    path(
        "admin/announcements/new/",
        views.new_announcement,
        name="skyward_expedition_new_announcement",
    ),
    path(
        "admin/announcements/<int:announcement_id>/edit/",
        views.edit_announcement,
        name="skyward_expedition_edit_announcement",
    ),
    path(
        "admin/announcements/<int:announcement_id>/delete/",
        views.delete_announcement,
        name="skyward_expedition_delete_announcement",
    ),
]
