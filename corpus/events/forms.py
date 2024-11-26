from django import forms
from corpus.forms import CorpusModelForm
from .models import Event

class EventForm(CorpusModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'poc': forms.SelectMultiple(attrs={
                'class': 'form-multiselect',
            }),
            'society': forms.SelectMultiple(attrs={
                'class': 'form-multiselect',
            }),
        }