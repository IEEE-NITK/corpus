from django import forms

from .models import Event
from corpus.forms import CorpusModelForm


class EventForm(CorpusModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "sigs",
            "description",
            "details",
            "start_date",
            "end_date",
            "page_link",
            "thumbnail",
        ]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "border p-2 w-full"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "border p-2 w-full"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # Check if end date is before start date
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "End date cannot be before start date.")

