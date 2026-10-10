from datetime import timedelta

from config.models import SIG
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

RECENT_WINDOW_DAYS = 60


class Event(models.Model):
    class StatusOverride(models.TextChoices):
        # TextChoices is like a enum
        # attribute = value, human readable text
        AUTO = "", "Automatic (by end date)"
        RECENT = "recent", "Force Recent"
        ARCHIVED = "archived", "Force Archived"

    name = models.CharField(max_length=200)
    page_link = models.URLField(max_length=400, null=True, blank=True)
    sigs = models.ManyToManyField(SIG, related_name="events", null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(verbose_name="Description",  null=True, blank=True)
    details = RichTextUploadingField(blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="newsletter/events/thumbnails", blank=True, null=True
    )
    status_override = models.CharField(
        max_length=10,
        choices=StatusOverride.choices, # [(val1, label1)...]
        default=StatusOverride.AUTO,
        blank=True,
        help_text="Leave Automatic unless this event must be pinned to a section.",
    )

    def __str__(self):
        return self.name

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now().date()

    @property
    def is_completed(self):
        return self.end_date < timezone.now().date()

    @property
    def status(self):
        """Lifecycle section: "current", "recent" or "archived"."""
        if self.status_override:
            return self.status_override
        today = timezone.localdate()
        if self.end_date >= today:
            return "current"
        # approximated as 60 days
        cutoff = today - timedelta(days=RECENT_WINDOW_DAYS)
        return "recent" if self.end_date >= cutoff else "archived"

    def clean(self):
        super().clean()

        if self.status_override == self.StatusOverride.RECENT and not self.thumbnail:
            raise ValidationError(
                {"thumbnail": "Thumbnail is required when showing in Recent Events."}
            )

    class Meta:
        ordering = ["-start_date"]
