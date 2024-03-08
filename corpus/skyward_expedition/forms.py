from django import forms
from skyward_expedition.models import Announcement
from skyward_expedition.models import Invite
from skyward_expedition.models import SEUser
from skyward_expedition.models import Submission
from skyward_expedition.models import Team

from corpus.forms import CorpusModelForm


class SEForm(CorpusModelForm):
    class Meta:
        model = SEUser
        fields = [
            "college_name",
            "degree",
            "year_of_study",
            "nitk_participant",
            "roll_number",
            "ieee_member",
            "ieee_number",
        ]

    def clean(self):
        data = self.cleaned_data
        if data.get("nitk_participant", None) and not data.get("roll_number", None):
            raise forms.ValidationError(
                "Enter your NITK roll number for verification that you are from NITK."
            )

        if data.get("ieee_member", None) and not data.get("ieee_number", None):
            raise forms.ValidationError(
                "Enter IEEE Membership number to verify membership status."
            )
        return data


class TeamCreationForm(CorpusModelForm):
    class Meta:
        model = Team
        fields = ["team_name"]


class InviteForm(CorpusModelForm):
    class Meta:
        model = Invite
        fields = ["invite_email"]


class AnnouncementForm(CorpusModelForm):
    ANNOUNCEMENT_OPTIONS = [
        ("1", "No email to be sent."),
        ("2", "Send email to all team leaders."),
        ("3", "Send email to all members"),
    ]
    announcement_mailing = forms.ChoiceField(
        widget=forms.Select, choices=ANNOUNCEMENT_OPTIONS
    )

    class Meta:
        model = Announcement
        fields = ["content", "url_link", "url_link_text", "announcement_mailing"]

    def clean(self):
        data = self.cleaned_data
        if data.get("url_link") and not data.get("url_link_text"):
            raise forms.ValidationError(
                "Both URL Link and corresponding text are required."
            )
        return data


class SubmissionForm(CorpusModelForm):
    class Meta:
        model = Submission
        fields = ["file"]
