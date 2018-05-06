from __future__ import unicode_literals
import binascii
import os
from django.conf import settings
from django.db import migrations


def generate_key():
    return settings.AUTH_SECRET_PREFIX + binascii.hexlify(os.urandom(20)).decode()


def forwards_func(apps, schema_editor):
    """
    We get the SecretToken and Client models from the versioned app registry.
    We get all the existing Clients, and create a new Secret Token for each of
    their related Users.
    """

    Client = apps.get_model("user_profiles", "Client")
    SecretToken = apps.get_model("tosp_auth", "SecretToken")

    db_alias = schema_editor.connection.alias

    # Get all the Clients
    Clients = Client.objects.using(db_alias).all()

    # Create a new SecretToken for every single one of the Clients
    for client in Clients:
        secret_token, created = SecretToken.objects.using(db_alias).get_or_create(key=generate_key(),
                                                                                  user=client.user)
        if not created:
            secret_token.delete()
            secret_token, created = SecretToken.objects.using(db_alias).get_or_create(key=generate_key(),
                                                                                      user=client.user)

def reverse_func(apps, schema_editor):
    """
    Reverse function should delete all the SecretTokens related to existing
    clients.
    """

    Client = apps.get_model("user_profiles", "Client")
    SecretToken = apps.get_model("tosp_auth", "SecretToken")

    db_alias = schema_editor.connection.alias

    # Get all the Clients
    Clients = Client.objects.using(db_alias).all()

    # Delete all the secret tokens for these Clients
    for client in Clients:
        SecretToken.objects.using(db_alias).filter(user=client.user).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('user_profiles', '0010_client_groups'),
        ('tosp_auth', '0002_auto_20171009_0240'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]