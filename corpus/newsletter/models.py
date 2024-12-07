from django.db import models
from blog.models import Post
from events.models import Event

# Create your models here.
class NewsPost(models.Model):
    date = models.DateField(auto_now_add=True, blank=True)
    event = models.OneToOneField(Event, related_name="newspost", blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/newsletter", blank=True)
    new = models.BooleanField(default=True, blank=True)

    class Meta:
        verbose_name = "News Post"
        verbose_name_plural = "News Posts"

    def __str__(self):
        return f"{self.event.title} - {self.date}"