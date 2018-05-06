from django.test import TestCase
from .utils import is_member
from .utils import CLIENT_GROUP
from .factories import ClientFactory


class TestClientModel(TestCase):
    """ Unit test suite for testing the Client model in .models

    Attributes:
    ----------
    self.user : django.contrib.auth.models.User
        A mock user to use across all tests.
    self.client : Client
        A mock client to use across all tests.
    """

    def setUp(self):
        """ Setup required for the tests in this suite.

        """
        self.client = ClientFactory.create()

    def test_client_save_group(self):
        """ Checks that when a new client is saved, it is a member of
        the Client group
        """
        self.assertTrue(is_member(self.client.user, [CLIENT_GROUP]))

    def test_str_client(self):
        """ Checks that this method __str__ method for the client returns
        the name of the user.
        """
        self.assertEqual(str(self.client), str(self.client.user))

    def test_inactive_save(self):
        """ Test that when a client is saved as inactive, the related user
        is deactivated as well.

        """
        self.assertTrue(self.client.user.is_active)
        self.client.active = False
        self.client.save()
        self.assertFalse(self.client.user.is_active)
