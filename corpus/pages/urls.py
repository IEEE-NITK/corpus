from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about_us/", views.about_us, name="about_us"),
    path("sig/<str:sig_name>/", views.sig, name="sig"),
    path("team", views.team, name="team"),
]
