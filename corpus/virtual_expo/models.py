from accounts.models import ExecutiveMember
from ckeditor_uploader.fields import RichTextUploadingField
from config.models import SIG
from django.db import models


# Create your models here.
class ReportType(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name


class Report(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    abstract = models.TextField(blank=False, null=False)
    thumbnail = models.ImageField(
        upload_to="virtual_expo/reports/thumbnails", blank=False, null=False
    )
    report_type = models.ForeignKey(
        ReportType, blank=False, null=False, on_delete=models.CASCADE
    )
    year = models.PositiveSmallIntegerField(blank=False, null=False)

    content = RichTextUploadingField(blank=False, null=False)

    ready_for_approval = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    approver = models.ForeignKey(
        ExecutiveMember, blank=True, null=True, on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def sigs(self):
        return SIG.objects.filter(executivemember__reportmember__report=self).distinct()


class ReportMember(models.Model):
    report = models.ForeignKey(
        Report, blank=False, null=False, on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        ExecutiveMember, blank=False, null=False, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("report", "member"),)

    def __str__(self):
        return f"{self.report} - {self.member}"
