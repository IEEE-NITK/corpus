# Generated by Django 5.1.3 on 2025-01-18 06:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0007_alter_executivemember_date_joined'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(choices=[('CompSoc', 'CompSoc'), ('Diode', 'Diode'), ('Piston', 'Piston')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layout', models.CharField(blank=True, max_length=20, null=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, null=True)),
                ('description', models.CharField(max_length=400)),
                ('author_github', models.CharField(blank=True, max_length=70)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('published_date', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.executivemember')),
                ('blog_tag', models.ManyToManyField(to='blog.tag')),
            ],
        ),
    ]
