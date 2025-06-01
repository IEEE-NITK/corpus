from django.urls import path
from smp import mentor_views as views

urlpatterns = [
    path("dashboard/", views.dashboard, name="smp_mentors_dashboard"),
    path("program/new/", views.new_program, name="smp_mentors_new_program"),
    path(
        "program/<int:program_id>/edit/",
        views.edit_program,
        name="smp_mentors_edit_program",
    ),
    path(
        "program/<int:program_id>/add_members/",
        views.add_members,
        name="smp_mentors_add_members",
    ),
    path(
        "program/<int:program_id>/upload/",
        views.uploads,
        name="smp_mentors_add_upload",
    ),
]
