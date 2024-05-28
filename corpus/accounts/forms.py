from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CorpusCreationForm(UserCreationForm):
    phone_no = forms.CharField(required=True, max_length=10)
    gender = forms.ChoiceField(choices=User.GENDERS, required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")

    error_css_class = "text-sm text-error"

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_no",
            "gender",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(CorpusCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs[
                "class"
            ] = "mt-1 block w-full rounded-md border-base-800 text-black shadow-sm focus:border-primary focus:ring focus:ring-primary-200 focus:ring-opacity-50"  # noqa: E501


class CorpusChangeForm(UserChangeForm):
    phone_no = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=User.GENDERS, required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_no",
            "gender",
            "email",
        ]


class CorpusLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CorpusLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs[
                "class"
            ] = "mt-1 block w-full rounded-md border-base-800 text-black shadow-sm focus:border-primary focus:ring focus:ring-primary-200 focus:ring-opacity-50"  # noqa: E501

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username:
            username = username.lower()
        return username


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "bg-gray-50 border\
                        border-gray-300\
                        text-white-900 text-sm rounded-lg \
                        focus:ring-blue-500 focus:border-blue-500\
                        block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 \
                        dark:placeholder-gray-400 dark:text-black \
                        dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "type": "email",
                "name": "email",
            }
        ),
    )
