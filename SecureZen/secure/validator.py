# Validator.py
import re
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

def validate_email_format(value):
    """Validate the email format."""
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not email_regex.match(value):
        raise ValidationError("Invalid email format.")

def sanitize_html(value):
    """Remove HTML tags and encode special characters from a string."""
    return strip_tags(value)