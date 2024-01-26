# Generated by Django 4.2.7 on 2024-01-26 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_executivemember_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='executivemember',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='executivemember',
            name='date_joined',
            field=models.DateTimeField(verbose_name='Date Joined'),
        ),
    ]
