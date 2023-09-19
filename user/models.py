import re
from core.models import BaseModel
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, phone, password, **other):
        if phone is None:
            raise ValueError("Please enter a phone number")

        user = self.model(phone=phone, **other)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **other) :
        other.setdefault('is_staff', True)
        other.setdefault('is_superuser', True)

        if other.get('is_staff') is not True :
            raise ValueError('Superuser must have is_staff=True.')
        if other.get('is_superuser') is not True :
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **other)


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
    def get_email_value(self, value):
        if value is None:
            return value
        try:
            regex = email_validator(value)
        except ValidationError:
            raise

        return regex
    

class PhoneNumberField(models.CharField):
    def get_phone_value(self, value):
        if value is None:
            return value
        try:
            regex = phone_validator(value)
        except ValidationError:
            raise

        return regex
    

class Address(BaseModel):
    address = models.TextField()

    def __str__(self):
        return self.address
    

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = EmailField(validators=[email_validator], unique=True)
    phone = PhoneNumberField(validators=[phone_validator], unique=True, max_length=20)
    password = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
