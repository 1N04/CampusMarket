from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser."""
    list_display = ('username', 'email', 'university', 'is_verified', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'university')
    search_fields = ('username', 'email', 'university')

    # Add custom fields to the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone_number', 'profile_picture', 'university', 'is_verified', 'bio'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'phone_number', 'university'),
        }),
    )
