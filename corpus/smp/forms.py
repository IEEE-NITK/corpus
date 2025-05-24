from accounts.models import User
from config.models import SIG
from django import forms
from smp.models import Program
from smp.models import ProgramMember
from smp.models import Submission
from smp.models import Upload

from corpus.forms import CorpusForm
from corpus.forms import CorpusModelForm


class ProgramFilterForm(CorpusForm):
    sig = forms.ChoiceField(choices=[])
    year = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(ProgramFilterForm, self).__init__(*args, **kwargs)

        sig_choices = [(0, "All SIGs"), (-1, "Inter-SIG")] + list(
            SIG.objects.values_list("id", "name")
        )
        year_choices = [(0, "All Years")] + [
            (x, x)
            for x in list(Program.objects.values_list("year", flat=True).distinct())
        ]

        self.fields["sig"].choices = sig_choices
        self.fields["year"].choices = year_choices


class ProgramForm(CorpusModelForm):
    class Meta:
        model = Program
        fields = [
            "title",
            "abstract",
            "thumbnail",
            "year",
            "description",
            "hide_program",
        ]


class ProgramMemberForm(CorpusModelForm):
    class Meta:
        model = ProgramMember
        fields = ["member"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        executive_users = User.objects.filter(executivemember__isnull=False).distinct()
        self.fields["member"].queryset = executive_users


class UploadForm(CorpusModelForm):
    class Meta:
        model = Upload
        fields = ["title", "upload_type", "content"]


class SubmissionForm(CorpusModelForm):
    class Meta:
        model = Submission
        fields = ["title", "link"]


class AdminProgramMemberForm(CorpusModelForm):
    class Meta:
        model = ProgramMember
        fields = ["member", "member_type"]
