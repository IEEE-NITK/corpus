from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetView
from django.urls import path

from .views import signin
from .views import signout
from .views import signup

urlpatterns = [
    path("signup/", signup, name="accounts_signup"),
    path("login/", signin, name="accounts_signin"),
    path("logout/", signout, name="accounts_signout"),
    path(
        "reset/",
        PasswordResetView.as_view(
            html_email_template_name="../templates/registration/password_reset_email.html"
        ),
        name="password_reset",
    ),
    path("reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]