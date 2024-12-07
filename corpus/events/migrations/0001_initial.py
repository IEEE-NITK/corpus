# Generated by Django 5.1.3 on 2024-12-07 05:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0007_alter_executivemember_date_joined'),
        ('config', '0004_sig_society_sigs'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Event Categories',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('registration_url', models.URLField(blank=True)),
                ('meeting_url', models.URLField(blank=True)),
                ('instagram_url', models.URLField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('location', models.CharField(max_length=32)),
                ('visibility', models.CharField(choices=[('i', 'Internal'), ('e', 'External')], max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_events', to='accounts.executivemember')),
                ('parent_event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_events', to='events.event')),
                ('poc', models.ManyToManyField(related_name='events', to='accounts.executivemember')),
                ('society', models.ManyToManyField(to='config.society')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=12)),
                ('source', models.URLField()),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objective', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('resources', models.JSONField(null=True)),
                ('student_turnout', models.IntegerField()),
                ('faculty_turnout', models.IntegerField(null=True)),
                ('photo_1', models.ImageField(upload_to='')),
                ('photo_2', models.ImageField(upload_to='')),
                ('iic_report_url', models.URLField(null=True)),
                ('dsw_report_url', models.URLField(null=True)),
                ('created_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='report_creator', to='accounts.executivemember')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('exec_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.executivemember')),
            ],
        ),
    ]
