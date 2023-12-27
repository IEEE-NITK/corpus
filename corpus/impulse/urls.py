from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="impulse_home"),
    path("index", views.index, name="impulse_index"),
    path("register", views.register, name="impulse_register"),
    path("create_team", views.create_team, name="impulse_create_team"),
    path("add_member", views.add_member, name="impulse_add_member2"),
    path("upload_payment_proof", views.upload_payment_proof, name="impulse_upload_payment_proof"),
    path("delete_payment_proof", views.delete_payment_proof, name="impulse_delete_payment_proof"),
    path("admin", views.admin, name="impulse_admin"),
    path("admin/teams", views.team_management, name="impulse_admin_teams"),
    path("admin/team/<int:pk>", views.team_page, name="impulse_admin_team_page"),
    path(
        "admin/team/<int:pk>/mark_payment_complete",
        views.mark_payment_complete,
        name="impulse_admin_mark_payment_complete",
    ),
    path(
        "admin/team/<int:pk>/mark_payment_incomplete",
        views.mark_payment_incomplete,
        name="impulse_admin_mark_payment_incomplete",
    ),
    path("admin/users", views.user_management, name="impulse_admin_users"),
    path(
        "admins/announcements",
        views.announcements_management,
        name="impulse_announcements",
    ),
    path(
        "admin/announcements/delete/<int:pk>",
        views.delete_announcement,
        name="impulse_delete_announcement",
    ),
]