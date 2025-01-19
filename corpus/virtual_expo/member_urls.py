from django.urls import path
from virtual_expo import member_views as views

urlpatterns = [
    path("dashboard/", views.dashboard, name="virtual_expo_members_dashboard"),
    path("report/new/", views.new_report, name="virtual_expo_members_new_report"),
    path(
        "report/<int:report_id>/edit/",
        views.edit_report,
        name="virtual_expo_members_edit_report",
    ),
    path(
        "report/<int:report_id>/add_members/",
        views.add_members,
        name="virtual_expo_members_add_members",
    ),
    path(
        "approver_dashboard/",
        views.approver_dashboard,
        name="virtual_expo_members_approver_dashboard",
    ),
]




