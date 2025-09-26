from django.urls import include
from django.urls import path
from smp import views

urlpatterns = [
    path("", views.home, name="smp_home"),
    path("<int:year>/", views.programs_by_year, name="smp_programs_by_year"),
    path("program/<int:program_id>", views.program, name="smp_program"),
    path(
        "preview/<int:program_id>/",
        views.preview_program,
        name="smp_preview_program",
    ),
    path("program/<int:program_id>/upload_list", views.upload_list, name="upload_list"),
    path(
        "program/upload/<int:upload_id>/submissions",
        views.view_submission,
        name="view_submission",
    ),
    path("program/<int:upload_id>/view/", views.view_upload, name="view_upload"),
    path(
        "program/upload/<int:upload_id>/submit",
        views.create_submission,
        name="create_submission",
    ),
    path("mentors/", include("smp.mentor_urls")),
    path("admin/", include("smp.admin_urls")),
]
