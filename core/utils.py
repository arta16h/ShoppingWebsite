from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

def get_phonenumber_regex():
    phone_regex = RegexValidator(
        regex=r"(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}", 
        message=_("invalid phone number")
    )
    return phone_regex