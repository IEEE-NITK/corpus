from django import forms
from corpus.forms import CorpusModelForm
from .models import Event

class EventForm(CorpusModelForm):
    required_css_class = 'required-field'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add an asterisk (*) to the labels of required fields
        for field_name, field in self.fields.items():
            if field.required:
                if field.label:
                    field.label = f"{field.label} *"
                else:
                    field.label = "*"

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time > end_time:
            raise forms.ValidationError("Start time cannot be later than end time!")
        
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ["created_by"]
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