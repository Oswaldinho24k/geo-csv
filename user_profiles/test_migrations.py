from django.test import TestCase
from django.contrib.auth.models import Group
from .utils import ADMIN_GROUP, CLIENT_GROUP


class TestLoadGroups(TestCase):
    """ Unit test suite for testing that initial data of
    Groups is created
    """

    def test_groups_created(self):
        """ Checks that this method __str__ method returns the name
        of the object.
        """
        self.assertTrue(Group.objects.get(name=ADMIN_GROUP))
        self.assertTrue(Group.objects.get(name=CLIENT_GROUP))
