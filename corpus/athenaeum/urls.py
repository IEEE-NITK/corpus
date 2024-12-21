from django.urls import path
from athenaeum import views

urlpatterns = [
    path("", views.home, name="athenaeum_home"),

]