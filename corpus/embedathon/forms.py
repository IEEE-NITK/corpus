from embedathon.models import EmbedathonUser

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
