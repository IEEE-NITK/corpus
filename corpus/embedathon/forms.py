from django import forms
from embedathon.models import Announcement
from embedathon.models import EmbedathonUser
from embedathon.models import Invite
from embedathon.models import Team

from corpus.forms import CorpusModelForm


class EmbedathonForm(CorpusModelForm):
    nitk_roll_number = forms.CharField(max_length=8, required=False)

    class Meta:
        model = EmbedathonUser
        fields = [
            "from_nitk",
            "college_name",
            "nitk_roll_number",
            "course",
            "year",
            "branch",
            "ieee_member",
            "ieee_membership_no",
            "cass_member",
        ]

    def clean(self):
        data = self.cleaned_data
        if data.get("from_nitk", None) and not data.get("nitk_roll_number", None):
            raise forms.ValidationError(
                "Enter your NITK Roll Number for verification that you are from NITK."
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
