from django.core.exceptions import ValidationError


def validate_geeks_mail(value):
    value = str(value)
    if len(value) == 13:
        return value
    else:
        raise ValidationError("need to be 13 digits written here")