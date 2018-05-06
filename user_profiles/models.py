from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from core.validators import PHONE_REGEX
from tosp_auth.models import SecretToken
from .utils import CLIENT_GROUP


class Client(models.Model):
    """ Extension of Django's User Model for Clients.

    We extend the Django User Model to identify Clients since they have relations with
    other models and close interaction with the API.

    Attributes:
    ----------
    CHOICE_MAGENTO : string
        Choice for Magento e-commerce platform
    CHOICE_PRESTASHOP : string
        Choice for Prestashop e-commerce platform
    CHOICE_SHOPIFY : string
        Choice for Shopify e-commerce platform
    CHOICE_WOO_COMMERCE : string
        Choice for WOO Commerce e-commerce platform
    CHOICE_PROPRIETARY = string
        Choice for proprietary e-commerce platform
    CHOICE_OTHER : string
        Choice for 'other' option for e-commerce platform
    CHOICES_STORE_BACKEND : tuple(tuple)
        These are the choices for the ecommerce_platform attribute
    user : django.contrib.auth.models.User
        The django User related to Client (i.e. contains the actual user information).
    active : BooleanField
        Indicates whether the profile is active or not.
    commercial_contact_name : CharField
        Name for the commercial contact at a client.
    commercial_contact_email : CharField
        Email for the commercial contact at a client.
    commercial_contact_phone : CharField
        Phone for the commercial contact at a client.
    legal_business_name : CharField
        Legal name under which a client's business is registered.
    rfc : CharField
        The RFC for a client.
    billing_address : CharField
        Billing address for a client.
    billing_email : CharField
        Billing email for a client.
    billing_phone : CharField
        Billing phone for a client.
    finance_contact_name : CharField
        Name for the finance contact at a client.
    finance_contact_email : CharField
        Email for the finance contact at a client.
    logistics_contact_name : CharField
        Name for the logistics contact at a client.
    logistics_contact_email : CharField
        Email for the logistics contact at a client.
    billing_conditions : CharField
        Billing conditions for a client.
    ecommerce_platform : CharField
        Name for the ecommerce platform a client uses.
    """

    CHOICE_MAGENTO = 'Magento'
    CHOICE_PRESTASHOP = 'Prestashop'
    CHOICE_SHOPIFY = 'Shopify'
    CHOICE_WOO_COMMERCE = 'WOO Commerce'
    CHOICE_PROPIETARY = 'Propietary'
    CHOICE_OTHER = 'Other'

    CHOICES_STORE_BACKEND = ((CHOICE_MAGENTO, 'Magento'),
                             (CHOICE_PRESTASHOP, 'Prestashop'),
                             (CHOICE_SHOPIFY, 'Shopify'),
                             (CHOICE_WOO_COMMERCE, 'WOO Commerce'),
                             (CHOICE_PROPIETARY, 'Propietaria'),
                             (CHOICE_OTHER, 'Otro'))

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    active = models.BooleanField(default=True)
    commercial_contact_name = models.CharField(max_length=255,
                                               blank=True,
                                               verbose_name='Nombre del Contacto Comercial')
    commercial_contact_email = models.EmailField(blank=True,
                                                 verbose_name='Email del Contacto Comercial')
    commercial_contact_phone = models.CharField(max_length=16,
                                                blank=True,
                                                validators=[PHONE_REGEX],
                                                verbose_name='Teléfono del Contacto Comercial')
    legal_business_name = models.CharField(max_length=500,
                                           blank=True,
                                           verbose_name='Razón Social')
    rfc = models.CharField(max_length=13,
                           blank=True,
                           verbose_name='RFC')
    billing_address = models.CharField(max_length=512,
                                       blank=True,
                                       verbose_name='Dirección de Facturación')
    billing_email = models.EmailField(blank=True,
                                      verbose_name='Email de Facturación')
    billing_phone = models.CharField(max_length=16,
                                     validators=[PHONE_REGEX],
                                     blank=True,
                                     verbose_name='Teléfono de Facturación')
    finance_contact_name = models.CharField(max_length=255,
                                            blank=True,
                                            verbose_name='Nombre del Contacto de Finanzas')
    finance_contact_email = models.EmailField(blank=True,
                                              verbose_name='Email del Contacto de Finanzas')
    logistics_contact_name = models.CharField(max_length=255,
                                              blank=True,
                                              verbose_name='Nombre del Contacto de Lógistica')
    logistics_contact_email = models.EmailField(blank=True,
                                                verbose_name='Email del Contacto de Lógistica')
    billing_conditions = models.TextField(blank=True,
                                          verbose_name='Condiciones de Facturación')
    ecommerce_platform = models.CharField(max_length=200,
                                          choices=CHOICES_STORE_BACKEND,
                                          blank=True,
                                          verbose_name='Plataforma de e-commerce')
    groups = models.ManyToManyField('waypoints.WaypointGroup', blank=True)

    def save(self, *args, **kwargs):
        """ Override the save method to add the client group.
        """
        user_group = Group.objects.get_or_create(name=CLIENT_GROUP)[0]
        self.user.groups.add(user_group)
        if not self.active:
            self.user.is_active = False
            self.user.save()
        if self.pk is None:
            token, created = Token.objects.get_or_create(user=self.user)
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        """ Return the string representation of the user
        related to this client.
        """
        return str(self.user)


@receiver(post_save, sender=Client)
def create_secret_token(sender, instance=None, created=False, **kwargs):
    """ Automatically create a new secret token for any new client created
    """
    if created:
        SecretToken.objects.create(user=instance.user)
