from django.urls import path

from . import views

urlpatterns = [
    path("", views.entwine_view, name="entwine_home"),
]
