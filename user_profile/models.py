from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
import hashlib

# ################################
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    def email_md5(self):
        return str(hashlib.md5(self.user.email.lower()).hexdigest())


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)




