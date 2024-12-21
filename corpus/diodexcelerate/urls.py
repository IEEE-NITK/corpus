from django.urls import path

from . import views

urlpatterns = [
    path("", views.diodexcelerate_view, name="diodexcelerate_home"),
]
