# Generated by Django 4.2.4 on 2023-12-27 09:59
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("embedathon", "0004_announcement"),
    ]

    operations = [
        migrations.AlterField(
            model_name="embedathonuser",
            name="year",
            field=models.CharField(
                choices=[("1", "1st Year"), ("2", "2nd Year"), ("3", "3rd Year")],
                max_length=1,
            ),
        ),
    ]
