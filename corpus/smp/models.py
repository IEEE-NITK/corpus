from accounts.models import ExecutiveMember
from accounts.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from config.models import SIG
from django.db import models

# Create your models here.


class Program(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    abstract = models.TextField(blank=False, null=False)
    thumbnail = models.ImageField(
        upload_to="virtual_expo/reports/thumbnails", blank=False, null=False
    )
    sig = models.ForeignKey(SIG, blank=False, null=False, on_delete=models.CASCADE)
    description = RichTextUploadingField(blank=False, null=False)
    year = models.PositiveSmallIntegerField(blank=False, null=False)
    hide_program = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def mentors(self):
        return ExecutiveMember.objects.filter(
            user__programmember__program=self, user__programmember__member_type="Mentor"
        ).distinct()

    def mentees(self):
        return ExecutiveMember.objects.filter(
            user__programmember__program=self, user__programmember__member_type="Mentee"
        ).distinct()


class ProgramMember(models.Model):
    MEMBER_TYPE_CHOICES = [
        ("Mentor", "Mentor"),
        ("Mentee", "Mentee"),
    ]
    program = models.ForeignKey(
        Program, blank=False, null=False, on_delete=models.CASCADE
    )
    member = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    member_type = models.CharField(
        max_length=10, choices=MEMBER_TYPE_CHOICES, blank=False, null=False
    )

    class Meta:
        unique_together = (("program", "member"),)

    def __str__(self):
        return f"{self.report} - {self.member}"


class Upload(models.Model):
    UPLOAD_TYPE_CHOICES = [("Assignment", "Assignment"), ("Resource", "Resource")]
    title = models.CharField(max_length=255, blank=False, null=False)
    upload_user = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )
    upload_type = models.CharField(
        max_length=10, choices=UPLOAD_TYPE_CHOICES, blank=False, null=False
    )
    content = RichTextUploadingField(blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.upload_type} by {self.upload_user} - {self.title}"

    def is_assignment(self):
        return self.upload_type == "Assignment"


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(
        Upload, on_delete=models.CASCADE, related_name="submissions"
    )
    link = models.URLField(blank=False, null=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user} for {self.assignment.title}"

    def clean(self):
        # Enforce that assignment is of type "Assignment"
        from django.core.exceptions import ValidationError

        if self.assignment.upload_type != "Assignment":
            raise ValidationError("You can only submit to an Assignment.")
