from django.urls import path
from smp import admin_views as views

urlpatterns = [
    path("dashboard/", views.dashboard, name="smp_admin_dashboard"),
    path(
        "program/<int:program_id>/add_members/",
        views.add_members,
        name="smp_admin_add_members",
    ),
    path("<int:program_id>/manage/", views.manage, name="smp_admin_manage"),
]
