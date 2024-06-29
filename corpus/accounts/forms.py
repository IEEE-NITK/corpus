from django import forms
from django.contrib.auth.forms import AuthenticationForm
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
            ] = "mt-1 w-full rounded-md shadow-sm"  # noqa: E501
            if visible.field.widget.input_type in ["text", "password", "email"]:
                visible.field.widget.attrs[
                    "class"
                ] += " input input-bordered focus:input-primary"
            elif visible.field.widget.input_type == "select":
                visible.field.widget.attrs[
                    "class"
                ] += " select select-bordered focus:select-primary"


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
            ] = "mt-1 w-full rounded-md shadow-sm"  # noqa: E501
            if visible.field.widget.input_type in ["text", "password", "email"]:
                visible.field.widget.attrs[
                    "class"
                ] += " input input-bordered focus:input-primary"

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username:
            username = username.lower()
        return username
