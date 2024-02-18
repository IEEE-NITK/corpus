from django import forms
from robotrix.models import Announcement
from robotrix.models import Invite
from robotrix.models import RobotrixUser
from robotrix.models import Team

from corpus.forms import CorpusModelForm


class RobotrixForm(CorpusModelForm):
    class Meta:
        model = RobotrixUser
        fields = [
            "from_nitk",
            "college_name",
            "roll_no",
            "ieee_member",
            "ieee_membership_no",
            "phone_no",
        ]

    def clean(self):
        data = self.cleaned_data
        if data.get("from_nitk", None) and not data.get("roll_no", None):
            raise forms.ValidationError(
                "Enter your roll number for verification that you are from NITK"
            )

        if data.get("ieee_member", None) and not data.get("ieee_membership_no", None):
            raise forms.ValidationError(
                "Enter your IEEE Membership Number for verification "
                + "that you are an IEEE member"
            )

        return data


class TeamCreationForm(CorpusModelForm):
    class Meta:
        model = Team
        fields = ["team_name"]


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
        fields = [
            "content",
            "url_link",
            "url_link_text",
            "announcement_type",
            "announcement_mailing",
        ]


class InviteForm(CorpusModelForm):
    class Meta:
        model = Invite
        fields = ["invite_email"]
