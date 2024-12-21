from django import forms
from farewell.models import Senior

from corpus.forms import CorpusModelForm


class SeniorForm(CorpusModelForm):
    class Meta:
        model = Senior
        fields = [
            "coming_farewell",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["coming_farewell"].widget.attrs["id"] = "check-5"
