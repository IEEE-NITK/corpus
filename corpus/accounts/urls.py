from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetView
from django.urls import path

from .views import signin
from .views import signout
from .views import signup
from .views import profile
from .views import edit_profile

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
    path("profile/<roll_no>", profile, name="accounts_profile"),
    path("profile/edit/<roll_no>", edit_profile, name="edit_profile")
]
