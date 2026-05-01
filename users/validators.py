import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UppercaseValidator:
    """Password must contain at least one uppercase letter (A-Z)."""

    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _('Your password must contain at least one uppercase letter (A–Z).'),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _('Your password must contain at least one uppercase letter (A–Z).')


class LowercaseValidator:
    """Password must contain at least one lowercase letter (a-z)."""

    def validate(self, password, user=None):
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _('Your password must contain at least one lowercase letter (a–z).'),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _('Your password must contain at least one lowercase letter (a–z).')


class DigitValidator:
    """Password must contain at least one digit (0-9)."""

    def validate(self, password, user=None):
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _('Your password must contain at least one number (0–9).'),
                code='password_no_digit',
            )

    def get_help_text(self):
        return _('Your password must contain at least one number (0–9).')


class SpecialCharacterValidator:
    """Password must contain at least one special character."""

    SPECIAL_CHARS = r'[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>/?`~]'

    def validate(self, password, user=None):
        if not re.search(self.SPECIAL_CHARS, password):
            raise ValidationError(
                _('Your password must contain at least one special character '
                  '(e.g. ! @ # $ % ^ & *).'),
                code='password_no_special',
            )

    def get_help_text(self):
        return _('Your password must contain at least one special character '
                 '(e.g. ! @ # $ % ^ & *).')


class NoWhitespaceValidator:
    """Password must not contain spaces."""

    def validate(self, password, user=None):
        if re.search(r'\s', password):
            raise ValidationError(
                _('Your password must not contain spaces.'),
                code='password_has_whitespace',
            )

    def get_help_text(self):
        return _('Your password must not contain spaces.')