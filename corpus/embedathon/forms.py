from embedathon.models import EmbedathonUser
from embedathon.models import Team

from corpus.forms import CorpusModelForm


class EmbedathonForm(CorpusModelForm):
    class Meta:
        model = EmbedathonUser
        fields = [
            "from_nitk",
            "college_name",
            "course",
            "year",
            "branch",
            "ieee_member",
            "ieee_membership_no",
            "cass_member",
        ]


class TeamCreationForm(CorpusModelForm):
    class Meta:
        model = Team
        fields = ["team_name"]
