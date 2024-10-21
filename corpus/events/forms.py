from django import forms
from .models import Event
from config.models import Society
from accounts.models import ExecutiveMember

# Create forms here

class EventForm(forms.Form):

    society = forms.ModelChoiceField(
        queryset=Society.objects.all(),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'}),
        empty_label="Select Society"
    )

    poc = forms.ModelChoiceField(
        queryset=ExecutiveMember.objects.all(),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'}),
        empty_label="Select POC"
    )

    meeting_url = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    instagram_url = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    linkedin_url = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    visibility = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=False)

    class Meta:
        model = Event
        fields = ('title', 
                  'description', 
                  'start_time', 
                  'end_time', 
                  'registration_url', 
                  'meeting_url',
                  'instagram_url',
                  'linkedin_url',
                  'location',
                  'category',
                  'society',
                  'visibility',
                  'poc',
                  'created_at')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input input-bordered w-full'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input input-bordered w-full'}),
            'registration_url': forms.URLInput(attrs={'class': 'input input-bordered w-full'}),
            'meeting_url': forms.URLInput(attrs={'class': 'input input-bordered w-full'}),
            'instagram_url': forms.URLInput(attrs={'class': 'input input-bordered w-full'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'input input-bordered w-full'}),
            'location': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'category': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'society': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'visibility': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'poc': forms.SelectMultiple(attrs={'class': 'select select-bordered w-full'}),
        }