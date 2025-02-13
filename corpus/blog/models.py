from accounts.models import ExecutiveMember
from django.db import models
from django.utils import timezone

TAG_CHOICES = [
    ("CompSoc", "CompSoc"),
    ("Diode", "Diode"),
    ("Piston", "Piston"),
]


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, choices=TAG_CHOICES)

    def __str__(self):
        return str(self.tag_name)


class Post(models.Model):
    blog_tag = models.ManyToManyField(Tag)
    layout = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(ExecutiveMember, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, null=True)
    description = models.CharField(max_length=400)
    author_github = models.CharField(max_length=70, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.title)