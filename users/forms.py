"""Forms for user registration, profile updates, and user management.

Defines forms for user creation, update, and profile editing.
"""

from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user account.

    Attributes:
      Meta: Model and fields for the form.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class CustomUserChangeForm(forms.ModelForm):
    """Form for updating an existing user account.

    Attributes:
      Meta: Model and fields for the form.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information.

    Attributes:
      Meta: Model and fields for the form.
    """
    class Meta:
        model = Profile
        fields = ['photo']
