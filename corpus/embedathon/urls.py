from django.urls import path
from embedathon import views

urlpatterns = [
    path("", views.index, name="embedathon_index"),
    path("register", views.register, name="embedathon_register"),
    path("create_team", views.create_team, name="embedathon_create_team"),
]
