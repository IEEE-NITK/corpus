from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.validators import RegexValidator


def validate_phone_number(value):
    if len(value) == 10:
        validator = RegexValidator(regex=r"^[0-9]{10}$")
        validator(value)
    elif len(value) == 12 and value.startswith("91"):
        validator = RegexValidator(regex=r"^91[0-9]{10}$")
        validator(value)
    elif len(value) == 13 and value.startswith("+91"):
        validator = RegexValidator(regex=r"^\+91[0-9]{10}$")
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
