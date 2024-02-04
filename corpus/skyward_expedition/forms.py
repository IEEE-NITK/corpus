from django import forms
from skyward_expedition.models import Announcement
from skyward_expedition.models import Invite
from skyward_expedition.models import SEUser
from skyward_expedition.models import Team

from corpus.forms import CorpusModelForm


class SEForm(CorpusModelForm):
    nitk_roll_number = forms.CharField(max_length=8, required=False)

    class Meta:
        model = SEUser
        fields = ["college_name"]


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
