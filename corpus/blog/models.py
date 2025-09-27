from accounts.models import ExecutiveMember
from ckeditor_uploader.fields import RichTextUploadingField
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
    text = RichTextUploadingField(blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)

    approved = models.BooleanField(default=False)
    approver = models.ForeignKey(
        ExecutiveMember,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="posts_approved",
    )
    ready_for_approval = models.BooleanField(default=False)

    def publish(self, approver=None):
        if self.approved and not self.published_date:
            self.published_date = timezone.now()

        if self.approved and not self.approver:
            self.approver = approver

        self.save()

    def __str__(self):
        return str(self.title)
