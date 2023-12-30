from impulse.models import ImpulseUser, Team, Announcement

from corpus.forms import CorpusModelForm

class ImpulseForm(CorpusModelForm):
    class Meta:
        model = ImpulseUser
        fields = [
            "from_nitk",
            "college_name",
            "roll_no",
            "ieee_member",
            "ieee_membership_no",
        ]
    
    def __init__(self, *args, **kwargs):
        super(ImpulseForm, self).__init__(*args, **kwargs)
        # set a required attribute based on conditions
        self.fields["college_name"].required = not self.fields['from_nitk'].widget.value_from_datadict(
            self.data, self.files, self.add_prefix('from_nitk')
        )
        self.fields["roll_no"].required = self.fields['from_nitk'].widget.value_from_datadict(
            self.data, self.files, self.add_prefix('from_nitk')
        )
        self.fields["ieee_membership_no"].required = self.fields['ieee_member'].widget.value_from_datadict(
            self.data, self.files, self.add_prefix('ieee_member')
        )

class TeamCreationForm(CorpusModelForm):
    class Meta:
        model = Team
        fields = ["team_name"]

class AnnouncementForm(CorpusModelForm):
    class Meta:
        model = Announcement
        fields = ["content", "url_link", "url_link_text", "announcement_type"]

class Member2Form(CorpusModelForm):
    class Meta:
        model = ImpulseUser
        fields = [
            "member2_name",
            "member2_email",
            "member2_from_nitk",
            "member2_college_name",
            "member2_roll_no",
            "member2_phone",
            "member2_ieee_member",
            "member2_ieee_membership_no",
        ]

class PaymentProofForm(CorpusModelForm):
    class Meta:
        model = Team
        fields = ["payment_proof"]
        