from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create_event", views.create_event, name="create_event"),
    path("manage_event/<int:pk>", views.manage_event, name="manage_event"),
    path("report/<int:pk>", views.report, name="report"),
]
