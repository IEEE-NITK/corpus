from accounts.models import User
from django.db import models

# Create your models here.

COURSES = [
    ("B", "B.Tech."),
    ("E", "B.E."),
    ("S", "B.Sc."),
    ("O", "Other undergraduate degree"),
]
YEAR = [("1", "1st Year"), ("2", "2nd Year"), ("3", "3rd Year")]
PAYMENT_STATUS = [("E", "Exempt"), ("U", "Fee Not Paid"), ("P", "Fee Paid")]


class EmbedathonUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    from_nitk = models.BooleanField(default=True)
    college_name = models.CharField(
        max_length=200, default="National Institute of Technology Karnataka"
    )
    course = models.CharField(max_length=1, choices=COURSES, blank=False, null=False)
    year = models.CharField(max_length=1, choices=YEAR, blank=False, null=False)
    branch = models.CharField(max_length=200, blank=False, null=False)
    ieee_member = models.BooleanField(default=False)
    ieee_membership_no = models.BigIntegerField(blank=True, null=True)
    cass_member = models.BooleanField(default=False)
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="team", blank=True, null=True
    )

    def __str__(self):
        return self.user.__str__()


class Team(models.Model):
    team_name = models.CharField(max_length=200, blank=False, null=False)
    team_leader = models.ForeignKey(
        EmbedathonUser, on_delete=models.CASCADE, related_name="leader"
    )
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS, blank=False, null=False, default="U"
    )

    def __str__(self):
        return self.team_name


class Invite(models.Model):
    inviting_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="invite_to_team"
    )
    invite_email = models.EmailField(blank=False, null=False)

    def __str__(self):
        return self.invite_email


class Announcement(models.Model):
    content = models.TextField(blank=False, null=False)
    url_link = models.URLField(blank=True, null=True)
    url_link_text = models.CharField(max_length=200, blank=True, null=True)
