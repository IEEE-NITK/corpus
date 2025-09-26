from django.urls import path

from . import views

urlpatterns = [
    path("", views.project_chimera_home, name="projectchimera_home"),
]
