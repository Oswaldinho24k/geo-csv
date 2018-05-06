"""
Provides various authentication policies.
"""

from rest_framework.authentication import TokenAuthentication
from .models import SecretToken


class SecretTokenAuthentication(TokenAuthentication):
    """
    Use token authentication as a base for the Secret Token.

    Change the secret keyword in order to identify the authentication method.
    """
    keyword = 'Secret'
    model = SecretToken
