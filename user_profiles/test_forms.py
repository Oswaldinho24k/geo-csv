from django.test import TestCase

from .factories import ClientFactory
from .forms import DeleteClientForm
from .models import Client


class ClientFormsTest(TestCase):
    """ Suite to test the forms related to the Client model.

    Attributes:
    -----------
    self.client : Client
        Client model to be used in all of the tests.
    """

    def setUp(self):
        """ Initialize all the attributes.

        """
        self.client = ClientFactory.create()

    def test_delete_form_clean(self):
        """ Test that the form is registered as clean
        when a valid id for a user is passed to it.

        """
        form = DeleteClientForm({'id_client': self.client.pk})
        self.assertTrue(form.is_valid())

    def test_delete_form_unclean(self):
        """ Test that a ValidationError is raised if
        an unexistent client is being eliminated.

        """
        invalid_id = 93
        form = DeleteClientForm({'id_client': invalid_id})
        self.assertFalse(form.is_valid())

    def test_delete_form_save(self):
        """ Test that the Client is inactive after the form is
        saved.

        """
        form = DeleteClientForm({'id_client': self.client.pk})
        self.assertTrue(form.is_valid())
        form.save()
        client = Client.objects.get(pk=self.client.pk)
        self.assertFalse(client.active)
