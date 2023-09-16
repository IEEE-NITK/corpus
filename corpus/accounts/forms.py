from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User, GENDERS

class CorpusCreationForm(UserCreationForm):
    phone_no = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=GENDERS, required=True)

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
            "password2"
        ]

    def __init__(self, *args, **kwargs):
        super(CorpusCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "mt-1 block w-full rounded-md border-base-800 text-black shadow-sm focus:border-primary focus:ring focus:ring-primary-200 focus:ring-opacity-50"

class CorpusChangeForm(UserChangeForm):
    phone_no = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=GENDERS, required=True)
    
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
            visible.field.widget.attrs["class"] = "mt-1 block w-full rounded-md border-base-800 text-black shadow-sm focus:border-primary focus:ring focus:ring-primary-200 focus:ring-opacity-50"

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.lower()
        return username