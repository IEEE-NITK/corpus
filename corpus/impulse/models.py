from django.db import models
from embedathon.models import PAYMENT_STATUS
from accounts.models import User

class ImpulseUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    from_nitk = models.BooleanField(default=True)
    college_name = models.CharField(
        max_length=200, default="National Institute of Technology Karnataka"
    )
    roll_no = models.CharField(max_length=8, blank=False, null=False)
    ieee_member = models.BooleanField(default=False)
    ieee_membership_no = models.BigIntegerField(blank=True, null=True)
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="team", blank=True, null=True
    )
    is_member2 = models.BooleanField(default=False)
    member2_name = models.CharField(max_length=200, blank=True, null=True)
    member2_email = models.EmailField(blank=True, null=True)
    member2_from_nitk = models.BooleanField(default=True)
    member2_college_name = models.CharField(
        max_length=200, default="National Institute of Technology Karnataka"
    )
    member2_roll_no = models.CharField(max_length=8, blank=True, null=True)
    member2_phone = models.CharField(max_length=13, blank=True, null=True)
    member2_ieee_member = models.BooleanField(default=False)
    member2_ieee_membership_no = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Team(models.Model):
    team_name = models.CharField(max_length=200, blank=False, null=False)
    team_leader = models.ForeignKey(
        ImpulseUser, on_delete=models.CASCADE, related_name="leader"
    )
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS, blank=False, null=False, default="U"
    )
    payment_proof = models.ImageField(upload_to="img/impulse/payment_proofs", blank=True, null=True)

    def __str__(self):
        return self.team_name
    
class Announcement(models.Model):
    content = models.TextField(blank=False, null=False)
    url_link = models.URLField(blank=True, null=True)
    url_link_text = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20] + "..."
