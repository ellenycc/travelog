"""Models for user accounts and profiles.

Defines CustomUser and Profile models for authentication and user data.
"""

import logging
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)

class CustomUser(AbstractUser):
    """Custom user model extending Django's AbstractUser.

    Attributes:
      is_staff: Whether the user is a staff member.
      is_active: Whether the user account is active.
    """
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Return the user's email address."""
        return self.email

class Profile(models.Model):
    """User profile with photo and following relationships.

    Attributes:
      user: The associated user account.
      photo: User's profile photo.
      follows: Users this profile follows.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to='profile_pics',
        blank=True,
        default='profile_pics/default.jpg'
    )
    follows = models.ManyToManyField(
        "self",
        related_name='followed_by',
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        """Return the username of the associated user."""
        return self.user.username  # type: ignore[attr-defined]

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Create or update a user profile when a CustomUser is saved.

    Args:
      sender: The model class that sent the signal.
      instance: The actual instance being saved.
      created: Whether this is a new instance.
      **kwargs: Additional keyword arguments.
    """
    try:
        Profile.objects.get_or_create(user=instance)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error("Error creating or updating profile for user %s (ID: %s): %s", instance, instance.id, e)