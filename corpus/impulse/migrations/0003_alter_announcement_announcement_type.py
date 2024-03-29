# Generated by Django 4.2.7 on 2024-01-06 18:33
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("impulse", "0002_remove_team_payment_proof"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="announcement_type",
            field=models.CharField(
                choices=[
                    ("A", "All Impulse Users"),
                    ("P", "Paid Teams"),
                    ("U", "Unpaid Teams"),
                    ("N", "Registered for Impulse but no team"),
                    ("NI", "Not Registered for Impulse"),
                ],
                default="A",
                max_length=2,
            ),
        ),
    ]
