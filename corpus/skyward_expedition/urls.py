from django.urls import path
from skyward_expedition import views

urlpatterns = [
    path("", views.home, name="skyward_expedition_home"),
]
