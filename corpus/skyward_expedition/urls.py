from django.urls import path
from skyward_expedition import views

urlpatterns = [
    path("", views.home, name="skyward_expedition_home"),
    path("register/", views.register, name="skyward_expedition_register"),
    path("dashboard/", views.dashboard, name="skyward_expedition_dashboard"),
]
