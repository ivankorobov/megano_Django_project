from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def profile_avatar_directory_path(instance: "Profile", filename: str):
    return "profile/{username}/avatar/{filename}".format(
        username=instance.user.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.TextField(max_length=30, null=False, blank=True, default="+88009995544")
    avatar = models.ImageField(null=True, blank=False, upload_to=profile_avatar_directory_path)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
