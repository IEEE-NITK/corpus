from django.db import models
from config.models import Society
from accounts.models import ExecutiveMember
from django.utils import timezone

# Create your models here.
class EventCategory(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Event Categories"

class Event(models.Model):
    VISIBILITIES = [
        ("i", "Internal"),
        ("e", "External"),
    ]
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(null=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    registration_url = models.URLField(blank=True)
    meeting_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    location = models.CharField(null=False, max_length=32)
    category = models.ForeignKey(EventCategory, null=False, on_delete=models.CASCADE)
    society = models.ManyToManyField(Society)
    visibility = models.CharField(max_length=8, choices=VISIBILITIES)
    poc = models.ManyToManyField(ExecutiveMember, related_name="events")
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)
    event_parent = models.ForeignKey('self', null=True, blank=True, related_name="sub_events", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} | {self.society.first().name}"

class Report(models.Model):
    event = models.OneToOneField(Event, null=False, on_delete=models.CASCADE)
    objective = models.CharField(max_length=128, null=False)
    description = models.TextField(null=False)
    resources = models.JSONField(null=True)
    student_turnout = models.IntegerField(null=False)
    faculty_turnout = models.IntegerField(null=True)
    photo_1 = models.ImageField(null=False)
    photo_2 = models.ImageField(null=False)
    iic_report_url = models.URLField(null=True)
    dsw_report_url = models.URLField(null=True)
    created_at = models.DateTimeField(null=False)
    created_by = models.ForeignKey(ExecutiveMember, null=True, on_delete=models.DO_NOTHING, related_name="report_creator")


class Volunteer(models.Model):
    event = models.ForeignKey(Event, null=False, on_delete=models.CASCADE)
    exec_member = models.ForeignKey(ExecutiveMember, null=False, on_delete=models.CASCADE)


class Budget(models.Model):
    event = models.OneToOneField(Event, null=False, on_delete=models.CASCADE)
    item = models.CharField(null=False, max_length=255)
    description = models.TextField()
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    source = models.URLField()

