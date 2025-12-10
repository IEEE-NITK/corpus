from accounts.models import User
from django.db import models

from corpus.tasks import send_email_async
from corpus.validators import FileValidator

file_validator = FileValidator(
    max_size=1024 * 1024 * 10,
    content_types=(
        "application/zip",
        "application/x-rar-compressed",
        "application/octet-stream",
    ),
)


# Create your models here.


class SEUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college_name = models.CharField(max_length=200)
    degree = models.CharField(
        max_length=200, blank=False, null=False, help_text="Degree Pursuing"
    )
    year_of_study = models.IntegerField(
        blank=False, null=False, help_text="Year of Study"
    )
    nitk_participant = models.BooleanField()
    roll_number = models.CharField(max_length=8, blank=True, null=True)
    ieee_member = models.BooleanField()
    ieee_number = models.CharField(max_length=20, blank=True, null=True)
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="team", blank=True, null=True
    )

    def __str__(self):
        return self.user.__str__()


class Team(models.Model):
    team_name = models.CharField(max_length=200, blank=False, null=False)
    team_leader = models.ForeignKey(
        SEUser, on_delete=models.CASCADE, related_name="leader"
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

    def send_email(self, mail_option):
        email_ids = None

        if mail_option == 2:
            email_ids = list(
                Team.objects.values_list("team_leader__user__email", flat=True)
            )
        elif mail_option == 3:
            email_ids = list(SEUser.objects.values_list("user__email", flat=True))

        if email_ids is not None:
            send_email_async.delay(
                "Announcement | Skyward Expedition",
                "emails/skyward_expedition/announcement.html",
                {"announcement": self},
                bcc=email_ids,
            )


class Submission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    file = models.FileField(
        verbose_name="Submission File",
        upload_to="skyward_expedition/submissions",
        validators=[file_validator],
    )
