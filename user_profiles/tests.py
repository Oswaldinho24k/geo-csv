from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from .utils import is_member, is_admin, is_client
from .models import Client
from .utils import ADMIN_GROUP, CLIENT_GROUP


class PermisosTestCase(TestCase):
    """ Suite to test the validation functions inside utils.py.

    This Suite tests the functions designed to validate permissions of users in order
    to grant them access to views across the project.

    Attributes:
    ----------
    user : django.contrib.auth.models.User
        A mock user to use across all tests.
    admin_group : django.contrib.auth.models.Group
        The group used to identify users that are admins.
    client_group: django.contrib.auth.models.Group.
        The group used to identify users that are clients.
    """

    def setUp(self):
        """ Initialize the attributes.
        """
        self.user = get_user_model().objects.create_user(
                                        username='some_user',
                                        email='temporary@gmail.com',
                                        password='some_pass')
        self.admin_group = Group.objects.get_or_create(name=ADMIN_GROUP)[0]
        self.client_group = Group.objects.get_or_create(name=CLIENT_GROUP)[0]

    def test_is_admin(self):
        """ Test if the is_admin works for the administrador group.

        Test if the is_admin function works properly for a user which has
        the administrador group, and also if the same user gets some other group.
        We expect is_admin to return True in both cases, since the user belongs
        to that group.
        """
        self.user.groups.add(self.admin_group)
        self.assertTrue(is_admin(self.user))
        self.user.groups.add(self.client_group)
        self.assertTrue(is_admin(self.user))

    def test_not_admin(self):
        """ Test if the is_admin fails for a user w/o the group.

        Test if the is_admin fails for a user which does not have the
        administrador group assigned. We also add a different group and check that
        is_admin fails again.
        """
        self.assertFalse(is_admin(self.user))
        self.user.groups.add(self.client_group)
        self.assertFalse(is_admin(self.user))

    def test_is_client(self):
        """ Test if the is_client works for the client group.

        Test if the is_client function works properly for a client.
        """
        client = Client.objects.create(user=self.user)
        self.assertTrue(is_client(client.user))

    def test_not_client(self):
        """ Test if the is_client fails for a user w/o the group.

        Test if the is_client fails for a user which does not have the
        client group assigned. We also add a different group and check that
        is_client fails again.
        """
        self.assertFalse(is_client(self.user))
        self.user.groups.add(self.admin_group)
        self.assertFalse(is_client(self.user))

    def test_is_member_invalid_group(self):
        """ Test if the is_member method fails for a non existing group.

        We validate that the is_member method returns false for a group
        that does not exist and is not assigned to the user.
        """
        self.assertFalse(is_member(self.user, ['blabla']))

    def test_is_member_multiple_groups(self):
        """ Test is_member with more than one group.

        Test that is_member validates correctly the existence of one group among others.
        That is, we check that a user who has one group: admin passes the test when we
        check against a list of more groups among which there is admin.
        """
        self.user.groups.add(self.admin_group)
        self.assertTrue(is_member(self.user, [CLIENT_GROUP, ADMIN_GROUP]))

    def test_is_not_member_multiple_groups(self):
        """ Test is_member with more than one group.

        Test that is_member fails when we ask if a user belongs to more than one group,
        when none of them is assigned to the user.
        """
        self.assertFalse(is_member(self.user, [ADMIN_GROUP, CLIENT_GROUP]))
