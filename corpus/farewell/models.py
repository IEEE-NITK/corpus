from django.db import models

# Create your models here.
class Senior(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    url_id = models.CharField(max_length=5, blank=False, null=False)
    email_id = models.EmailField(max_length=50, blank=False, null=True)
    coming_farewell = models.BooleanField(default=False)

    def __str__(self):
        return self.name
