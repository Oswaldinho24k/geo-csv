import binascii
import os

from django.conf import settings
from django.db import models


class SecretToken(models.Model):
    """
    This token is utilized for authentication with a system
    that should never be openly shared.

    This token is used in a similar way to the way stripe
    validates its API requests with it's libraries. The ones
    that are open and need to be done from public places such
    as a js page from the users webrowser use the regular token
    authentication. The ones that actually confirm, create and
    send vital information for price calculation use this token
    to authenticate.
    """
    key = models.CharField(max_length=60, primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='secret_token',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(SecretToken, self).save(*args, **kwargs)

    def generate_key(self):
        return settings.AUTH_SECRET_PREFIX + binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
