from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.validators import RegexValidator


def validate_phone_number(value):
    validator = RegexValidator(regex=r"^\+?[0-9]{8,14}$")
    validator(value)


def validate_nitk_email(value):
    email_validator = EmailValidator(message="Email must end with @nitk.edu.in")
    if not value.endswith("@nitk.edu.in"):
        raise ValidationError("Email must end with @nitk.edu.in")
    email_validator(value)


def validate_roll_number(value):
    NITK_ROLL_NUMBER_REGEX = r"^[1-9][0-9]{2}[A-Z]{2}[0-9]{3}$"
    roll_number_validator = RegexValidator(
        regex=NITK_ROLL_NUMBER_REGEX,
        message="Roll number should follow the format: 201XX123",
    )
    roll_number_validator(value)


def validate_reg_number(value):
    NITK_REG_NUMBER_REGEX = r"^[0-9]{6,}$"
    reg_number_validator = RegexValidator(
        regex=NITK_REG_NUMBER_REGEX,
        message="Registration number should follow the format: 2010723",
    )
    reg_number_validator(value)


def validate_ieee_number(value):
    IEEE_NUMBER_REGEX = r"^[0-9]{8,}$"
    ieee_number_validator = RegexValidator(
        regex=IEEE_NUMBER_REGEX,
        message="IEEE Membership number should follow the format: 97240288",
    )
    ieee_number_validator(value)


def validate_ieee_email(value):
    email_validator = EmailValidator(message="Email must end with @ieee.org")
    if not value.endswith("@ieee.org"):
        raise ValidationError("Email must end with @ieee.org")
    email_validator(value)

def validate_image(image):
    file_size = image.file.size
    limit = 5 * 1024 * 1024  # 5 MB limit
    if file_size > limit:
        raise ValidationError("Image size exceeds 5MB.")

