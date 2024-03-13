from config.models import SIG
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .validators import validate_ieee_email
from .validators import validate_ieee_number
from .validators import validate_nitk_email
from .validators import validate_phone_number
from .validators import validate_reg_number
from .validators import validate_roll_number


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError(_("Email must be set."))

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **kwargs)

    def users(self):
        return self.filter(is_active=True)


class User(AbstractUser):
    GENDERS = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("N", "Prefer not to disclose"),
    ]

    username = None
    phone_no = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="Phone Number",
        validators=[validate_phone_number],
    )
    gender = models.CharField(max_length=1, choices=GENDERS)
    email = models.EmailField(unique=True, verbose_name="Personal Email")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        phone = str(self.phone_no)
        if len(phone) == 12 and phone.startswith("91"):
            self.phone_no = phone[2:]
        elif len(phone) == 13 and phone.startswith("+91"):
            self.phone_no = phone[3:]

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ExecutiveMember(models.Model):
    NITK_DEPARTMENTS = [
        ("WO", "Water Resources and Ocean Engineering"),
        ("CH", "Chemical Engineering"),
        ("CM", "Chemistry"),
        ("CV", "Civil Engineering"),
        ("CS", "Computer Science and Engineering"),
        ("EE", "Electrical and Electronics Engineering"),
        ("EC", "Electronics and Communication Engineering"),
        ("IT", "Information Technology"),
        ("MA", "Mathematical and Computational Sciences"),
        ("ME", "Mechanical Engineering"),
        ("MT", "Metallurgical and Materials Engineering"),
        ("MN", "Mining Engineering"),
        ("PS", "Physics"),
        ("SM", "School of Humanities, Social Sciences and Management"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    sig = models.ForeignKey(SIG, on_delete=models.CASCADE)
    edu_email = models.EmailField(
        unique=True, verbose_name="NITK EDU Email", validators=[validate_nitk_email]
    )
    roll_number = models.CharField(
        max_length=8,
        unique=True,
        verbose_name="NITK Roll Number",
        validators=[validate_roll_number],
    )
    reg_number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="NITK Registration Number",
        validators=[validate_reg_number],
    )
    minor_branch = models.CharField(
        max_length=2,
        choices=NITK_DEPARTMENTS,
        blank=True,
        null=True,
        verbose_name="Minor Branch",
    )
    ieee_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="IEEE Membership Number",
        validators=[validate_ieee_number],
    )
    ieee_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="IEEE Email",
        validators=[validate_ieee_email],
    )
    linkedin = models.URLField(
        blank=True, null=True, verbose_name="Linkedin Profile URL"
    )

    profile_picture = models.ImageField(
        blank=True, null=True, upload_to="accounts/executivemember/profile_picture"
    )
    # TODO: Phase out with GitHub OAuth details
    github = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="GitHub Username"
    )
    is_nep = models.BooleanField(default=False, verbose_name="Is NEP Member?")
    date_joined = models.DateTimeField(verbose_name="Date Joined", default=now)

    def save(self, *args, **kwargs):
        self.roll_number = self.roll_number.upper()

        super(ExecutiveMember, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} [{self.sig.name}]"


class Core(models.Model):

    POST_CHOICES = (
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
    )
    executivemember = models.OneToOneField(
        ExecutiveMember, null=False, on_delete=models.CASCADE
    )
    post = models.IntegerField(null=False, choices=POST_CHOICES)
    sig = models.ForeignKey(SIG, null=False, on_delete=models.CASCADE)
    term_start = models.DateField()
    term_end = models.DateField()

    def __str__(self):
        self_user = self.executivemember.user
        return f"{self_user.first_name} {self_user.last_name}"

    def get_post_display(self):
        return dict(Core.POST_CHOICES).get(self.post)


class Faculty(models.Model):
    class Meta:
        verbose_name_plural = "faculties"

    FACULTY_POSTS = (
        ("Branch Counselor", "Branch Counselor"),
        ("CIS Faculty Advisor", "CIS Faculty Advisor"),
        ("CompSoc Faculty Advisor", "CompSoc Faculty Advisor"),
        ("CAS Faculty Advisor", "CAS Faculty Advisor"),
        ("SPS Faculty Advisor", "SPS Faculty Advisor"),
        ("Photonic Society Faculty Advisor", "Photonic Society Faculty Advisor"),
        ("WIE Faculty Advisor", "WIE Faculty Advisor"),
        ("IAS Faculty Advisor", "IAS Faculty Advisor"),
        ("SIGHT Chair", "SIGHT Chair"),
        ("RAS Faculty Advisor", "RAS Faculty Advisor"),
        ("GRSS Faculty Advisor", "GRSS Faculty Advisor"),
    )
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    sig = models.ForeignKey(SIG, null=False, on_delete=models.CASCADE)
    post = models.CharField(
        max_length=100, null=False, choices=FACULTY_POSTS, blank=True
    )
    term_start = models.DateField()
    term_end = models.DateField()
    website = models.URLField(max_length=200, null=True, blank=True)
