from django.urls import path

from .views import about_us
from .views import index
from .views import impulse

urlpatterns = [
    path("", index, name="index"),
    path("about_us/", about_us, name="about_us"),
    path('impulse', impulse, name='impulse'),
]
