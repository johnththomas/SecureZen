from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from secure.models import User
# Custom Validator for URLs using Django's built-in URLValidator
def validate_url(value):
    """Validate the given URL using Django's URLValidator."""
    validator = URLValidator()
    try:
        validator(value)
    except ValidationError:
        raise ValidationError(f"{value} is not a valid URL")

class FileScan(models.Model):
    file_name = models.CharField(max_length=255)
    scan_id = models.CharField(max_length=255)
    scan_result = models.JSONField(null=True, blank=True)  # Stores the JSON response
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'file_scan_custom_user'

    def __str__(self):
        return self.file_name

class URLScan(models.Model):
    url = models.URLField(max_length=500, validators=[validate_url])
    scan_id = models.CharField(max_length=255)
    scan_result = models.JSONField(null=True, blank=True)
    scanned_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'URL_scan_custom_user'

    def __str__(self):
        return self.url


