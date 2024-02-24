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
]
