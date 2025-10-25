from config.models import SIG
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=200)
    page_link = models.URLField(max_length=400, null=True, blank=True)
    sigs = models.ManyToManyField(SIG, related_name="events", null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    archive_event = models.BooleanField(default=False)
    show_in_recent = models.BooleanField(default=False)
    thumbnail = models.ImageField(
        upload_to="newsletter/events/thumbnails", blank=True, null=True
    )

    def __str__(self):
        return self.name

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now().date()

    @property
    def is_completed(self):
        return self.end_date < timezone.now().date()

    def clean(self):
        super().clean()

        if self.show_in_recent and not self.thumbnail:
            raise ValidationError(
                {"thumbnail": "Thumbnail is required when showing in Recent Events."}
            )

    class Meta:
        ordering = ["-start_date"]
