from athenaeum import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="athenaeum_home"),
]
