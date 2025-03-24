from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_approved', True)
        
        # Force the role to 'admin' for superusers
        extra_fields.setdefault('role', 'admin')
        
        return super().create_superuser(username, email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    is_approved = models.BooleanField(default=False)  # Approval status for the user
    objects = CustomUserManager()

    def get_role_display(self):
        return dict(self.ROLE_CHOICES).get(self.role, "Unknown Role")
    
