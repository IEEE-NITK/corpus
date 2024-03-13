# Generated by Django 4.2.10 on 2024-03-12 17:07
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_remove_core_user_core_executivemember_and_more"),
    ]

    operations = [
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
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]
