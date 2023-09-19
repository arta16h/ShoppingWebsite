import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

EMAIL_REGEX_PATTERN = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
PHONE_REGEX_PATTERN = r"(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}"

def email_validator(email) :
    if not (matched := re.fullmatch(EMAIL_REGEX_PATTERN, email.strip())):
        raise ValidationError("Invalid Email!")
    return matched

def phone_validator(phone):
    if not (matched := re.fullmatch(PHONE_REGEX_PATTERN, phone.strip())):
        raise ValidationError("Invalid phone number!")
    return matched

class EmailField(models.CharField):
    def get_value(self, value):
        if value is None:
            return value
        try:
            regex = email_validator(value)
        except ValidationError:
            raise

        return regex

class User(AbstractBaseUser):
    email = EmailField(validators=[email_validator], unique=True)
    phone = models.CharField(max_length=14)
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    address = models.ForeignKey(on_delete=models.CASCADE)
