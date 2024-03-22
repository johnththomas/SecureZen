from django.apps import AppConfig


class SecureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'secure'

"""
default_auto_field Setting: This line sets the default_auto_field attribute of the FreezingConfig class.
This attribute specifies the default primary key field for models in the app. In this case, it's set to 'django.db.models.BigAutoField', 
which means that Django will use a 64-bit integer as the primary key field, suitable for databases that support large auto-incrementing integers.
"""
