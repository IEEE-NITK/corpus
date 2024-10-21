from django.db import models
from config.models import Society
from accounts.models import ExecutiveMember

# Create your models here.
class Event(models.Model):
    CATEGORIES = [
        ("KSS", "KSS"),
        ("COMPETITION", "Competition"),
        ("EXPERT_LECTURE", "Expert Lecture"),
        ("WORKSHOP", "Workshop"),
        ("HACKATHON", "Hackathon"),
    ]

    VISIBILITIES = [
        ("INTERNAL", "Internal"),
        ("EXTERNAL", "External"),
    ]
    title = models.CharField(max_length=128, blank=False)
    description = models.TextField(null=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    registration_url = models.URLField(null=False, unique=True)
    meeting_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    location = models.CharField(null=False, max_length=32)
    category = models.CharField(null=False, choices=CATEGORIES)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    visibility = models.CharField(blank=True, choices=VISIBILITIES)
    poc = models.ManyToManyField(ExecutiveMember, related_name="events")
    created_at = models.DateTimeField(null=False)

    def __str__(self):
        return f"{self.title} | {self.society.name}"


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


class Volunteer(models.Model):
    event = models.ForeignKey(Event, null=False, on_delete=models.CASCADE)
    exec_member = models.OneToOneField(ExecutiveMember, null=False, on_delete=models.CASCADE)


class Budget(models.Model):
    event = models.OneToOneField(Event, null=False, on_delete=models.CASCADE)
    item = models.CharField(null=False, max_length=255)
    description = models.TextField()
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    source = models.URLField()

