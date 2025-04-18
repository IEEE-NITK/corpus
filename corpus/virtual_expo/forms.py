from config.models import SIG
from django import forms
from virtual_expo.models import Report
from virtual_expo.models import ReportMember
from virtual_expo.models import ReportType

from corpus.forms import CorpusForm
from corpus.forms import CorpusModelForm


class ReportFilterForm(CorpusForm):
    report_type = forms.ChoiceField(choices=[])
    sig = forms.ChoiceField(choices=[])
    year = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(ReportFilterForm, self).__init__(*args, **kwargs)

        report_type_choices = [(0, "All Report Types")] + list(
            ReportType.objects.values_list("id", "name")
        )
        sig_choices = [(0, "All SIGs"), (-1, "Inter-SIG")] + list(
            SIG.objects.values_list("id", "name")
        )
        year_choices = [(0, "All Years")] + [
            (x, x)
            for x in list(Report.objects.values_list("year", flat=True).distinct())
        ]

        self.fields["report_type"].choices = report_type_choices
        self.fields["sig"].choices = sig_choices
        self.fields["year"].choices = year_choices


class ReportForm(CorpusModelForm):
    class Meta:
        model = Report
        fields = ["title", "abstract", "thumbnail", "report_type", "year", "content"]


class AdminReportForm(CorpusModelForm):
    class Meta:
        model = Report
        fields = [
            "title",
            "abstract",
            "thumbnail",
            "report_type",
            "year",
            "content",
            "ready_for_approval",
            "approver",
            "approved",
            "created_at",
            "approved_at",
        ]


class ReportMemberForm(CorpusModelForm):
    class Meta:
        model = ReportMember
        fields = ["member"]
