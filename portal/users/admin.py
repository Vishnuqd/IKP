from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Optionally configure list display, search fields, etc.
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    # If you have custom fields, you can extend fieldsets here
