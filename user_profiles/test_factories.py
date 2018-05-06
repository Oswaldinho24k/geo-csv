from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from .factories import UserFactory, ClientFactory
from .models import Client
from .utils import ADMIN_GROUP, CLIENT_GROUP, is_admin, is_client


class UserFactoryTest(TestCase):
    """ Suite to test the user factories, as well as it's ability to add a model.

    Attributes:
    ----------
    user : django.contrib.auth.models.User
        A mock user to use across all tests.
    admin_group : django.contrib.auth.models.Group
        The group used to identify users that are administradores.
    """

    def setUp(self):
        """ Initialize the attributes.
        """
        self.admin_group = Group.objects.get_or_create(name=ADMIN_GROUP)[0]
        self.client_group = Group.objects.get_or_create(name=CLIENT_GROUP)[0]

    def test_new_user(self):
        """ Test if the user factory can create a vanilla user with no groups.

        """
        user = UserFactory.create()
        self.assertIsInstance(user, get_user_model())

    def test_new_user_with_groups(self):
        """ Test if the validator returns a string of the appropriate size, when
        passed a numerical argument.

        """
        user = UserFactory.create(groups=(self.admin_group,))
        self.assertIsInstance(user, get_user_model())
        self.assertTrue(is_admin(user))


class ClientFactoryTest(TestCase):
    """ Suite to test the client factory.

    Attributes:
    -----------
    PHONE_REGEX : RegexValidator
        This validator checks that phone numbers are properly formatted.
    """

    def test_new_client(self):
        """ Test if the crypto_secure string generator, creates a 12 char
        string, when given no arguments.

        """
        client = ClientFactory.create()
        self.assertIsInstance(client, Client)
        self.assertTrue(is_client(client.user))
