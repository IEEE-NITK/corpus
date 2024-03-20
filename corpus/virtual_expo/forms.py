from config.models import SIG
from django import forms
from virtual_expo.models import ReportType

from corpus.forms import CorpusForm


class ReportFilterForm(CorpusForm):
    report_type_choices = [(0, "All Report Types")] + list(
        ReportType.objects.values_list("id", "name")
    )
    sig_choices = [(0, "All SIGs"), (-1, "Inter-SIG")] + list(
        SIG.objects.values_list("id", "name")
    )

    report_type = forms.ChoiceField(choices=report_type_choices)
    sig = forms.ChoiceField(choices=sig_choices)
