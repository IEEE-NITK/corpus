from django.urls import path
from .views import signup, signin, signout

urlpatterns = [
    path("signup/", signup, name="accounts_signup"),
    path("login/", signin, name="accounts_signin"),
    path("logout/", signout, name="accounts_signout")
]