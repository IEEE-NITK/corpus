# Generated by Django 4.2.7 on 2024-08-17 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_executivemember_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='accounts/profile/pics'),
        ),
        migrations.AlterField(
            model_name='executivemember',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 17, 17, 14, 23, 410838, tzinfo=datetime.timezone.utc), verbose_name='Date Joined'),
        ),
    ]
