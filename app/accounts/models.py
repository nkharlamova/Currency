import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static


def upload_avatar(instance, filename):
    return f'{instance.id}/avatars/{filename}'


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        permissions = [
            ("can_change_email", "Can change the user email"),
        ]

    email = models.EmailField('email address', unique=True)
    avatar = models.FileField(upload_to=upload_avatar, default=None, null=True, blank=True)
    phone = models.CharField(max_length=64, default=None, null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(uuid.uuid4())

        super().save(*args, **kwargs)

    def avatar_url(self):
        if self.avatar:
            return self.avatar.url

        return static('img/anon_user.jpg')
