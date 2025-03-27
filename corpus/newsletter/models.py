from django.db import models

# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    timing = models.TimeField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | {self.start_date} - {self.end_date}"
    

class Event(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    image = models.ImageField(null=False, blank=True, upload_to="newsletter/images")
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | {self.date}"

