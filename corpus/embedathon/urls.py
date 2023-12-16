from django.urls import path
from embedathon import views

urlpatterns = [
    path("", views.home, name="embedathon_home"),
    path("index", views.index, name="embedathon_index"),
    path("register", views.register, name="embedathon_register"),
    path("create_team", views.create_team, name="embedathon_create_team"),
    path("create_invite", views.create_invite, name="embedathon_create_invite"),
    path(
        "accept_invite/<int:pk>", views.accept_invite, name="embedathon_accept_invite"
    ),
    path(
        "delete_invite/<int:pk>", views.delete_invite, name="embedathon_delete_invite"
    ),
    path("admin", views.admin, name="embedathon_admin"),
    path("admin/teams", views.team_management, name="embedathon_admin_teams"),
    path("admin/team/<int:pk>", views.team_page, name="embedathon_admin_team_page"),
    path(
        "admin/team/<int:pk>/mark_payment_complete",
        views.mark_payment_complete,
        name="embedathon_admin_mark_payment_complete",
    ),
]
