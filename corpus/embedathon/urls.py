from django.urls import path
from embedathon import views

urlpatterns = [
    path("", views.index, name="embedathon_index"),
    path("register", views.register, name="embedathon_register"),
    path("create_team", views.create_team, name="embedathon_create_team"),
    path("create_invite", views.create_invite, name="embedathon_create_invite"),
    path(
        "accept_invite/<int:pk>", views.accept_invite, name="embedathon_accept_invite"
    ),
    path(
        "delete_invite/<int:pk>", views.delete_invite, name="embedathon_delete_invite"
    ),
]
