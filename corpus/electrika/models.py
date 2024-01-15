from django.db import models
from embedathon.models import PAYMENT_STATUS
from accounts.models import User

class ElectrikaUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    from_nitk = models.BooleanField(default=True)
    college_name = models.CharField(
        max_length=200, default="National Institute of Technology Karnataka"
    )
    roll_no = models.CharField(max_length=8, blank=True, null=True)
    ieee_member = models.BooleanField(default=False)
    ieee_membership_no = models.BigIntegerField(blank=True, null=True)
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="team", blank=True, null=True
    )
    to_be_teamed_up = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
    
class Team(models.Model):
    team_name = models.CharField(max_length=200, blank=False, null=False)
    team_leader = models.ForeignKey(
        ElectrikaUser, on_delete=models.CASCADE, related_name="leader"
    )
    def __str__(self):
        return self.team_name
    
class Announcement(models.Model):

    AnnouncementType = (
        ("A", "All Electrika Users"),
        ("T", "All Electrika Teams"),
        ("N", "Registered for Electrika but no team"),
    )

    content = models.TextField(blank=False, null=False)
    url_link = models.URLField(blank=True, null=True)
    url_link_text = models.CharField(max_length=200, blank=True, null=True)
    announcement_type = models.CharField(max_length=2, choices=AnnouncementType, blank=False, null=False, default="A")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20] + "..."

class Invite(models.Model):
    inviting_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="invite_to_team"
    )
    invite_email = models.EmailField(blank=False, null=False)

    def __str__(self):
        return self.invite_email