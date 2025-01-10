from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

from .models import User
from .models import ExecutiveMember


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

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_no', 'gender', 'email', 'profile_pic']
        widgets = {
            'phone_no': forms.TextInput(attrs={'class': 'rounded-lg border-gray-300 bg-base-200'}),
            'gender': forms.Select(attrs={'class': 'rounded-lg border-gray-300 bg-base-200'}),
            'email': forms.EmailInput(attrs={'class': 'rounded-lg border-gray-300 bg-base-200'}),
            'profile_pic': forms.ClearableFileInput(attrs={'multiple': False}),

        }

class ExecutiveMemberForm(forms.ModelForm):
    class Meta:
        model = ExecutiveMember
        fields = [
            'edu_email', 'roll_number', 'reg_number', 'minor_branch',
            'ieee_number', 'ieee_email', 'linkedin', 'github', 'is_nep'
        ]
        widgets = {
            'edu_email': forms.EmailInput(attrs={'class': 'rounded-lg border-gray-300 bg-base-200', 'required': True}),
            'roll_number': forms.TextInput(attrs={'class': 'rounded-lg border-gray-300 bg-base-200', 'required': True}),
            'reg_number': forms.TextInput(attrs={'class': 'rounded-lg border-gray-300 bg-base-200', 'required': True}),
            'minor_branch': forms.Select(attrs={'class': 'rounded-lg border-gray-300 bg-base-200 w-full',}),
            'ieee_number': forms.TextInput(attrs={'class': 'rounded-lg border-gray-300 bg-base-200','required': True}),
            'ieee_email': forms.EmailInput(attrs={'class': 'rounded-lg border-gray-300 bg-base-200'}),
            'linkedin': forms.URLInput(attrs={'class': 'rounded-lg border-gray-300 bg-base-200'}),
            'github': forms.TextInput(attrs={'class': 'rounded-lg border-gray-300 bg-base-200'}),
            'is_nep': forms.CheckboxInput(),
        }