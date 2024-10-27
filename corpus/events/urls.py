from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("new", views.new, name="new"),
    path("manage_event/<int:pk>", views.manage_event, name="manage_event"),
    path("report/<int:pk>", views.report, name="report"),
]
