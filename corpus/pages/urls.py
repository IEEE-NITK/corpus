from django.urls import path
from pages import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about_us/", views.about_us, name="about_us"),
    path("impulse", views.impulse, name="impulse"),
    path("sig/<str:sig_slug>/", views.sig, name="sig"),
]
