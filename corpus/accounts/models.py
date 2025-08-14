from config.models import SIG
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validators import validate_ieee_email
from .validators import validate_ieee_number
from .validators import validate_nitk_email
from .validators import validate_phone_number
from .validators import validate_reg_number
from .validators import validate_roll_number
from corpus.validators import validate_image


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
    profile_pic = models.ImageField(
        upload_to="profile/pics",
        validators=[validate_image],
        blank=True,
        null=True,
        default=None,
    )

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

    # TODO: Phase out with GitHub OAuth details
    github = models.CharField(
        max_length=39, blank=True, null=True, verbose_name="GitHub Username"
    )
    hide_github = models.BooleanField(default=False)
    hide_linkedin = models.BooleanField(default=False)
    is_nep = models.BooleanField(default=False, verbose_name="Is NEP Member?")
    date_joined = models.DateTimeField(
        default=timezone.localtime, verbose_name="Date Joined"
    )

    def save(self, *args, **kwargs):
        self.roll_number = self.roll_number.upper()

        super(ExecutiveMember, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} [{self.sig.name}]"
