# Generated by Django 4.2.4 on 2023-11-13 17:31
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("config", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="society",
            name="description",
            field=models.TextField(default="", verbose_name="Description"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="society",
            name="name",
            field=models.CharField(
                choices=[
                    ("AESS", "Aerospace and Electronic Systems Society"),
                    ("APS", "Antennas and Propagation Society"),
                    ("BTS", "Broadcast Technology Society"),
                    ("CASS", "Circuits and Systems Society"),
                    ("COM", "Communications Society"),
                    ("CIS", "Computational Intelligence Society"),
                    ("CS", "Computer Society"),
                    ("CTS", "Consumer Technology Society"),
                    ("CSS", "Control Systems Society"),
                    ("DEIS", "Dielectrics and Electrical Insulation Society"),
                    ("ES", "Education Society"),
                    ("ECS", "Electromagnetic Compatibility Society"),
                    ("EDS", "Electron Devices Society"),
                    ("EPS", "Electronics Packing Society"),
                    ("EMBS", "Engineering in Medicine and Biology Society"),
                    ("GRSS", "Geoscience and Remote Sensing Society"),
                    ("IES", "Industrial Electronics Society"),
                    ("IAS", "Industry Applications Society"),
                    ("ITS", "Information Theory Society"),
                    ("IMS", "Instrumentation and Measurement Society"),
                    ("ITSS", "Intelligent Transportation Systems Society"),
                    ("MS", "Magnetics Society"),
                    ("MTTS", "Microwave Theory and Technology Society"),
                    ("NPSS", "Nuclear and Plasma Sciences Society"),
                    ("OES", "Oceanic Engineering Society"),
                    ("PHO", "Photonics Society"),
                    ("PELS", "Power Electronics Society"),
                    ("PES", "Power and Energy Society"),
                    ("PSES", "Product Safety Engineering Society"),
                    ("PCS", "Professional Communication Society"),
                    ("RS", "Reliability Society"),
                    ("RAS", "Robotics and Automation Society"),
                    ("SPS", "Signal Processing Society"),
                    ("SSIT", "Society on Social Implications of Technology"),
                    ("SSCS", "Solid-State Circuits Society"),
                    ("SMCS", "Systems, Man, and Cybernetics Society"),
                    ("TEMS", "Technology and Engineering Management Society"),
                    (
                        "UFFCS",
                        "Ultrasonics, Ferroelectrics, and Frequency Control Society",
                    ),
                    ("VT", "Vehicular Technology Society"),
                    ("SIGHT", "Special Interest Group on Humanitarian Technology"),
                    ("WIE", "Women in Engineering"),
                ],
                max_length=5,
                unique=True,
                verbose_name="Name",
            ),
        ),
    ]
