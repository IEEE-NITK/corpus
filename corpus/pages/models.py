from accounts.models import User
from django.db import models


class Achievement(models.Model):
    title = models.CharField(max_length=128, verbose_name="Title")
    date = models.DateField(verbose_name="Date of Achievement")
    url = models.URLField(blank=True, null=True, verbose_name="Related URL")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Related User",
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name="Description")

    def __str__(self):
        return self.title


class Tag(models.Model):
    TAGS = [
        ("GSOC", "Google Summer of Code"),
        ("IAS SRFP", "IAS Summer Research Fellowship Program"),
        ("SB", "Student Branch Award"),
        # TODO: Add more tags
    ]

    tag = models.CharField(max_length=32, choices=TAGS, verbose_name="Tag")
    achievement = models.ForeignKey(
        Achievement, on_delete=models.CASCADE, verbose_name="Achievement"
    )


class Publication(models.Model):
    title = models.CharField(max_length=256, verbose_name="Title")
    date = models.DateField(verbose_name="Publish Date")
    url = models.URLField(verbose_name="URL")
    authors = models.CharField(max_length=256, verbose_name="Authors")
    source = models.CharField(max_length=512, verbose_name="Source")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Related User",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title
