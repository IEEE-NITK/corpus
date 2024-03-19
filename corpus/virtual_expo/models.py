from accounts.models import ExecutiveMember
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class ReportType(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name


class Report(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    abstract = models.CharField(max_length=200, blank=False, null=False)
    thumbnail = models.ImageField(
        upload_to="virtual_expo/reports/thumbnails", blank=False, null=False
    )
    content = CKEditor5Field(config_name="extends", blank=False, null=False)
    year = models.PositiveSmallIntegerField(blank=False, null=False)
    report_type = models.ForeignKey(
        ReportType, blank=False, null=False, on_delete=models.CASCADE
    )

    ready_for_approval = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    approver = models.ForeignKey(
        ExecutiveMember, blank=True, null=True, on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class ReportMember(models.Model):
    member = models.ForeignKey(
        ExecutiveMember, blank=False, null=False, on_delete=models.CASCADE
    )
    report = models.ForeignKey(
        Report, blank=False, null=False, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.report} - {self.member}"
