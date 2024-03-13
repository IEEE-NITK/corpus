# Generated by Django 4.2.10 on 2024-03-13 16:58
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_executivemember_date_joined_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="core",
            name="user",
        ),
        migrations.AddField(
            model_name="core",
            name="executivemember",
            field=models.OneToOneField(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.executivemember",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="faculty",
            name="website",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="core",
            name="post",
            field=models.IntegerField(
                choices=[
                    (1, "Convenor"),
                    (2, "Chairperson"),
                    (3, "Vice Chairperson"),
                    (4, "Secretary"),
                    (5, "Joint Secretary"),
                    (6, "Treasurer(Branch)"),
                    (7, "Treasurer(Institute)"),
                    (8, "Webmaster"),
                    (9, "Media Lead"),
                    (10, "Outreach Lead"),
                    (11, "Envision Lead"),
                    (12, "Labs Lead"),
                    (13, "CompSoc Chair"),
                    (14, "CompSoc Vice Chair"),
                    (15, "CompSoc Secretary"),
                    (16, "CompSoc Project Head"),
                    (17, "CompSoc Project Coordinator"),
                    (18, "CIS Chair"),
                    (19, "CIS Secretary"),
                    (20, "CIS Project Head"),
                    (21, "Diode Chair"),
                    (22, "SPS Chair"),
                    (23, "SPS Vice Chair"),
                    (24, "SPS Secretary"),
                    (25, "CAS Chair"),
                    (26, "CAS Vice Chair"),
                    (27, "CAS Secretary"),
                    (28, "RAS Chair"),
                    (29, "RAS Secretary"),
                    (30, "Piston Chair"),
                    (31, "Piston Vice Chair"),
                    (32, "Piston Secretary"),
                    (33, "IAS Chair"),
                    (34, "IAS Secretary"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="core",
            name="term_end",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="core",
            name="term_start",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="post",
            field=models.CharField(
                blank=True,
                choices=[
                    ("BRANCH COUNSELOR", "Branch Counselor"),
                    ("CIS FACULTY ADVISOR", "CIS Faculty Advisor"),
                    ("COMPSOC FACULTY ADVISOR", "CompSoc Faculty Advisor"),
                    ("CAS FACULTY ADVISOR", "CAS Faculty Advisor"),
                    ("SPS FACULTY ADVISOR", "SPS Faculty Advisor"),
                    (
                        "PHOTONIC SOCIETY FACULTY ADVISOR",
                        "Photonic Society Faculty Advisor",
                    ),
                    ("WIE FACULTY ADVISOR", "WIE Faculty Advisor"),
                    ("IAS FACULTY ADVISOR", "IAS Faculty Advisor"),
                    ("SIGHT CHAIR", "SIGHT Chair"),
                    ("RAS FACULTY ADVISOR", "RAS Faculty Advisor"),
                    ("GRSS FACULTY ADVISOR", "GRSS Faculty Advisor"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="term_end",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="faculty",
            name="term_start",
            field=models.DateField(),
        ),
    ]
