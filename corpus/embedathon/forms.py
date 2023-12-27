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
        if data.get("from_nitk", None) and data.get("nitk_roll_number", None):
            return data
        else:
            raise forms.ValidationError(
                "Enter your NITK Roll Number for verification that you are from NITK."
            )


class TeamCreationForm(CorpusModelForm):
    class Meta:
        model = Team
        fields = ["team_name"]


class InviteForm(CorpusModelForm):
    class Meta:
        model = Invite
        fields = ["invite_email"]


class AnnouncementForm(CorpusModelForm):
    class Meta:
        model = Announcement
        fields = ["content", "url_link", "url_link_text"]
