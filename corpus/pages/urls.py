from django.urls import path

from .views import about_us
from .views import index
from .views import sig
from .views import embedathon

urlpatterns = [
    path("", index, name="index"),
    path("about_us/", about_us, name="about_us"),
    path("<str:sig_name>/", sig, name="sig"),
]
