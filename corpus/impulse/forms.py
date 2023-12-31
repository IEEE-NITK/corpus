from impulse.models import ImpulseUser, Team, Announcement
from django import forms
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

    def clean(self):
        data = self.cleaned_data
        if data.get("from_nitk", None) and not data.get("roll_no", None):
            raise forms.ValidationError(
                "Enter your roll number for verification that you are from NITK"
            )
        
        if data.get("ieee_member", None) and not data.get("ieee_membership_no", None):
            raise forms.ValidationError(
                "Enter your IEEE Membership Number for verification that you are an IEEE member"
            )
        
        return data

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
        model = Team
        fields = [
            "member_name",
            "member_email",
            "member_from_nitk",
            "member_college_name",
            "member_roll_no",
            "member_phone",
            "member_ieee_member",
            "member_ieee_membership_no",
        ]

class PaymentProofForm(CorpusModelForm):
    class Meta:
        model = Team
        fields = ["payment_proof"]
        