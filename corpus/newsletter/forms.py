from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from corpus.forms import CorpusForm
from corpus.forms import CorpusModelForm
from .models import *

class AnnouncementForm(CorpusModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'start_date', 'end_date', 'timing', 'link']
        widgets = {
                'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'border p-2 w-full'}),
                'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'border p-2 w-full'}),
                'timing': forms.TimeInput(attrs={'type': 'time', 'class': 'border p-2 w-full'}),
        }


class EventForm(CorpusModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'image']