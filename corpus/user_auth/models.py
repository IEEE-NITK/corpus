from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CorpusUser(AbstractUser):
    phone = PhoneNumberField()
