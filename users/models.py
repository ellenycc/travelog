from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    pass

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to='profile_pics',
        blank=True,
        default='profile_pics/default.jpg'
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)
