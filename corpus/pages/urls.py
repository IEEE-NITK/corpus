from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about_us/", views.about_us, name="about_us"),
    path("sig/<str:sig_name>/", views.sig, name="sig"),
    path("sig-dashboard/", views.sig_dashboard_list, name="sig_dashboard_list"),
    path(
        "sig-dashboard/<slug:sig_slug>/",
        views.sig_dashboard,
        name="sig_dashboard",
    ),
    path("team/", views.team, name="team"),
]
