# Generated by Django 4.2.7 on 2024-06-29 06:03
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tag_name",
                    models.CharField(
                        choices=[
                            ("CompSoc", "CompSoc"),
                            ("Diode", "Diode"),
                            ("Piston", "Piston"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("layout", models.CharField(max_length=20)),
                ("title", models.CharField(max_length=200)),
                ("description", models.CharField(max_length=300)),
                ("author_github", models.CharField(max_length=70)),
                ("text", models.TextField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("published_date", models.DateTimeField(blank=True, null=True)),
                ("blog_tag", models.ManyToManyField(to="blog.tag")),
            ],
        ),
    ]
