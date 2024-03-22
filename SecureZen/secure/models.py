from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Avatar')
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="custom_user_groups",  # unique related name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_permissions",  # unique related name
        related_query_name="user",
    )

    class Meta:
        db_table = 'custom_user'  # This changes the database table name

    def __str__(self):
        return self.username
    
class HomePageContent(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    content = models.TextField(verbose_name="Content")

    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Contents"

    def __str__(self):
        return self.title
