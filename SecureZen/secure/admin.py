# Import necessary modules and classes from Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

# Customizing the UserAdmin for the User model
class UserAdmin(BaseUserAdmin):
    # Define the sections and fields for the User model in the admin interface
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'image', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # Define the fields displayed in the admin list view for the User model
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # Enable search functionality for specified fields
    search_fields = ('username', 'first_name', 'last_name', 'email')
    # Enable filtering by specified fields in the admin interface
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    # Enable a horizontal filter interface for 'groups' and 'user_permissions'
    filter_horizontal = ('groups', 'user_permissions',)

# Register the User model with the customized UserAdmin
admin.site.register(User, UserAdmin)
