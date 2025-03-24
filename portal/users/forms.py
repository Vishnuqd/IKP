from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Dynamically remove 'admin' from the choices in the registration form
        self.fields['role'].choices = [
            (role, label) for role, label in CustomUser.ROLE_CHOICES if role != 'admin'
        ]

        # Add Bootstrap styling to each form field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
