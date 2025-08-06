from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile when a new User is created,
    or update the profile if the user is saved.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
