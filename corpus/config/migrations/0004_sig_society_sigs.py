# Generated by Django 4.2.7 on 2024-01-06 17:44
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0003_moduleconfiguration"),
    ]

    operations = [
        migrations.CreateModel(
            name="SIG",
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
                    "name",
                    models.CharField(max_length=10, unique=True, verbose_name="Name"),
                ),
                ("about", models.TextField(default="", verbose_name="About Us")),
                ("what_we_do", models.TextField(default="", verbose_name="What We Do")),
                ("slug", models.SlugField(null=True, unique=True)),
            ],
            options={
                "verbose_name": "SIG",
                "verbose_name_plural": "SIGs",
            },
        ),
        migrations.AddField(
            model_name="society",
            name="sigs",
            field=models.ManyToManyField(related_name="societies", to="config.sig"),
        ),
    ]


# Generated by Django 4.2.4 on 2023-12-22 08:12
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0003_moduleconfiguration"),
    ]

    operations = [
        migrations.CreateModel(
            name="SIG",
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
                    "name",
                    models.CharField(max_length=10, unique=True, verbose_name="Name"),
                ),
                ("about", models.TextField(default="", verbose_name="About Us")),
                ("what_we_do", models.TextField(default="", verbose_name="What We Do")),
                ("slug", models.SlugField(null=True, unique=True)),
            ],
            options={
                "verbose_name": "SIG",
                "verbose_name_plural": "SIGs",
            },
        ),
        migrations.AddField(
            model_name="society",
            name="sigs",
            field=models.ManyToManyField(related_name="societies", to="config.sig"),
        ),
    ]
