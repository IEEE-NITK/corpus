from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="electrika_home"),
    path("index", views.index, name="electrika_index"),
    path("register", views.register, name="electrika_register"),
    path("create_team", views.create_team, name="electrika_create_team"),
    path("create_invite", views.create_invite, name="electrika_create_invite"),
    path("accept_invite/<int:pk>", views.accept_invite, name="electrika_accept_invite"),
    path("delete_invite/<int:pk>", views.delete_invite, name="electrika_delete_invite"),
    path("teamify/optin", views.opt_in, name="electrika_opt_in"),
    path("teamify/optout", views.opt_out, name="electrika_opt_out"),
    path("admin", views.admin, name="electrika_admin"),
    path("admin/teams", views.team_management, name="electrika_admin_teams"),
    path(
        "admin/teams/create",
        views.create_team_admin,
        name="electrika_admin_team_create",
    ),
    path("admin/team/<int:pk>", views.team_page, name="electrika_admin_team_page"),
    path("admin/users", views.user_management, name="electrika_admin_users"),
    path(
        "admins/announcements",
        views.announcements_management,
        name="electrika_announcements",
    ),
    path(
        "admin/announcements/delete/<int:pk>",
        views.delete_announcement,
        name="electrika_delete_announcement",
    ),
    path(
        "admin/team/download_csv",
        views.team_download,
        name="electrika_admin_download_teams_csv",
    ),
]
