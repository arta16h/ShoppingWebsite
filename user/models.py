import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

EMAIL_REGEX_PATTERN = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"

def email_validator(email) :
    if not (matched := re.fullmatch(EMAIL_REGEX_PATTERN, email.strip())):
        raise ValidationError("Invalid Email!")
    return matched

class User(AbstractBaseUser):
    email=models.EmailField()
    phone=models.CharField(max_length=14)
    username=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=100)
    password=models.CharField(max_length=50)
    address=models.ForeignKey(on_delete=models.CASCADE)
