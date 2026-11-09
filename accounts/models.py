from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model for CampusMarket."""
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Phone Number')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Profile Picture')
    university = models.CharField(max_length=200, blank=True, verbose_name='University')
    is_verified = models.BooleanField(default=False, verbose_name='Verified')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Bio')

    def __str__(self):
        return self.username
