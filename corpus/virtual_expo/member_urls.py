from django.urls import path
from virtual_expo import member_views as views

urlpatterns = [
    path("dashboard/", views.dashboard, name="virtual_expo_members_dashboard"),
    path(
        "preview/<int:report_id>/",
        views.preview_report,
        name="virtual_expo_members_preview_report",
    ),
    path("report/new/", views.new_report, name="virtual_expo_members_new_report"),
]
