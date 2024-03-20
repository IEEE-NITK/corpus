from config.models import SIG
from django import forms
from virtual_expo.models import Report
from virtual_expo.models import ReportType

from corpus.forms import CorpusForm
from corpus.forms import CorpusModelForm


class ReportFilterForm(CorpusForm):
    report_type_choices = [(0, "All Report Types")] + list(
        ReportType.objects.values_list("id", "name")
    )
    sig_choices = [(0, "All SIGs"), (-1, "Inter-SIG")] + list(
        SIG.objects.values_list("id", "name")
    )

    report_type = forms.ChoiceField(choices=report_type_choices)
    sig = forms.ChoiceField(choices=sig_choices)


class ReportForm(CorpusModelForm):
    class Meta:
        model = Report
        fields = ["title", "abstract", "thumbnail", "report_type", "year", "content"]
