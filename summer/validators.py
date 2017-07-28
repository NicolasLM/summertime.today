import re

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
import pytz
from pytz.exceptions import UnknownTimeZoneError


@deconstructible
class UsernameValidator(validators.RegexValidator):
    """ASCII validator.

    Only accepts ASCII letters, numbers and . and -.
    """
    regex = r"""
    ^                  # beginning of string
    (?![-.])           # no - or . at the beginning
    (?!.*[.-]{2})      # no __ or _. or ._ or .. or -- inside
    [a-zA-Z0-9.-]+     # allowed characters, at least one must be present
    (?<![.-])          # no - or . at the end
    $                  # end of string
    """
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers, and . and - characters.'
    )
    flags = re.X


def timezone_exists_validator(value):
    try:
        pytz.timezone(value)
    except UnknownTimeZoneError:
        raise ValidationError(
            _('%(value)s is not a valid timezone name'),
            params={'value': value},
        )


def iata_code_validator(value: str):
    if len(value) != 3 and not value.isupper():
        raise ValidationError(
            _('%(value)s is not a valid IATA code'),
            params={'value': value},
        )


validators = [UsernameValidator()]
