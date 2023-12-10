from accounts.models import User
from django.db import models

# Create your models here.

COURSES = [("B", "B.Tech."), ("M", "M.Tech."), ("P", "PhD")]


class EmbedathonUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    from_nitk = models.BooleanField(default=True)
    college_name = models.CharField(
        max_length=200, default="National Institute of Technology Karnataka"
    )
    course = models.CharField(max_length=1, choices=COURSES)
    year = models.IntegerField(blank=False, null=False)
    branch = models.CharField(max_length=200, blank=False, null=False)
    ieee_member = models.BooleanField(default=False)
    ieee_membership_no = models.BigIntegerField(blank=True, null=True)
    cass_member = models.BooleanField(default=False)

    def __str__(self):
        return self.user.__str__()
