from django.urls import path
from user_auth import views

urlpatterns = [
    path("login/", views.login, name="login"),
]
