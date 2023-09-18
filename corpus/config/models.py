from django.db import models


class Society(models.Model):
    """
    Society Model.
    Defines all societies that are part of IEEE NITK SB.
    """

    IEEE_SOCIETIES = [
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
        ("UFFCS", "Ultrasonics, Ferroelectrics, and Frequency Control Society"),
        ("VT", "Vehicular Technology Society"),
    ]
    name = models.CharField(
        verbose_name="Name", max_length=5, unique=True, choices=IEEE_SOCIETIES
    )
    url = models.URLField(verbose_name="URL", max_length=200, unique=True)
    image = models.ImageField(verbose_name="Image", upload_to="img/logo/")
    dark_image = models.ImageField(
        verbose_name="Dark Image", upload_to="img/logo/", blank=True, null=True
    )

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = "Society"
        verbose_name_plural = "Societies"
