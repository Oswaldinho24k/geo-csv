from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache


class Waypoint(models.Model):
    """ Base structure for the app.

    We extend the Django User Model to identify Clients since they have relations with
    other models and close interaction with the API.

    Attributes:
    ----------
    CHOICE_OTHER : string
        Choice for 'other' option for e-commerce platform
    CHOICES_STORE_BACKEND : tuple(tuple)
        These are the choices for the ecommerce_platform attribute
    user : django.contrib.auth.models.User
        The django User related to Client (i.e. contains the actual user information).
    active : BooleanField
        Indicates whether the profile is active or not.
    """

    active = models.BooleanField(default=True, verbose_name='Activo')
    address = models.OneToOneField('logistics.Address')
    carriers = models.ManyToManyField('logistics.Carrier', blank=True)
    contact_email = models.EmailField(blank=True,
                                      verbose_name='Email del Contacto')
    contact_last_name = models.CharField(max_length=255,
                                         blank=True,
                                         verbose_name='Apellido del Contacto')
    contact_name = models.CharField(max_length=255,
                                    blank=True,
                                    verbose_name='Nombre del Contacto')
    contact_phone = models.CharField(max_length=16,
                                     blank=True,
                                     verbose_name='Teléfono del Contacto')
    contact_phone_extension = models.CharField(max_length=8,
                                               blank=True,
                                               verbose_name='Extensión Teléfono del Contacto')
    deleted = models.BooleanField(default=False)
    entity = models.ForeignKey('waypoints.Entity', null=True)
    external_id = models.CharField(max_length=35,
                                   unique=True,
                                   verbose_name='Id del Punto en API Externa')
    holiday_time_end = models.TimeField(blank=True,
                                        null=True,
                                        verbose_name='Fin Horario Dia Festivos')
    holiday_time_start = models.TimeField(blank=True,
                                          null=True,
                                          verbose_name='Inicio Horario Dia Festivos')
    lunch_break = models.BooleanField(default=False, verbose_name='Pausa Almuerzo')
    lunch_time_end = models.TimeField(blank=True,
                                      null=True,
                                      verbose_name='Fin Pausa Almuerzo')
    lunch_time_start = models.TimeField(blank=True,
                                        null=True,
                                        verbose_name='Inicio Pausa Almuerzo')
    name = models.CharField(max_length=255,
                            blank=False,
                            verbose_name='Nombre del Punto de Entrega')
    latitude = models.DecimalField(max_digits=12,
                                   decimal_places=9,
                                   blank=False,
                                   verbose_name='Latitud')
    longitude = models.DecimalField(max_digits=12,
                                    decimal_places=9,
                                    blank=False,
                                    verbose_name='Longitud')
    open_holidays = models.BooleanField(default=False, verbose_name='Abierto Dias Festivos')
    open_saturday = models.BooleanField(default=False, verbose_name='Abierto Sabados')
    saturday_time_end = models.TimeField(blank=True,
                                         null=True,
                                         verbose_name='Fin Horario Sabados')
    saturday_time_start = models.TimeField(blank=True,
                                           null=True,
                                           verbose_name='Inicio Horario Sabados')
    time_open = models.TimeField(blank=False,
                                 null=True,
                                 verbose_name='Horario Apertura')
    time_close = models.TimeField(blank=False,
                                  null=True,
                                  verbose_name='Horario Cierre')
    volume_limit = models.DecimalField(max_digits=5,
                                       decimal_places=2,
                                       default=10.0,
                                       verbose_name='Limitación Volumétrica')

    def __str__(self):
        """ Return the string representation of the user
        related to this client.
        """
        return '{entity} - {name}'.format(entity=self.entity, name=self.name)


@receiver(post_save, sender=Waypoint, dispatch_uid="clear_waypoints_all_cache")
@receiver(post_delete, sender=Waypoint, dispatch_uid="clear_waypoints_all_cache")
def delete_waypoints_cache(sender, instance, **kwargs):
    cache.delete('waypoints_all')


class WaypointGroup(models.Model):
    active = models.BooleanField(default=True, verbose_name='Activo')
    name = models.CharField(max_length=255,
                            blank=False,
                            verbose_name='Nombre del Grupo')
    entities = models.ManyToManyField('waypoints.Entity', blank=True)

    def __str__(self):
        """ Return the string representation of the user
        related to this client.
        """
        return self.name


class Entity(models.Model):
    name = models.CharField(max_length=255,
                            blank=False,
                            verbose_name='Nombre de la Entidad')

    def save(self, *args, **kwargs):
        """ Override the save method to add the carriers.
        If entities are created through migrations via a get_or_create,
        this method is not called, this will be useful when we want to
        create entities via a form.
        """
        created = False
        if self.pk is None:
            god_group = WaypointGroup.objects.get(name='Todos')
            created = True
        super(Entity, self).save(*args, **kwargs)
        if created:
            god_group.entities.add(self)
            god_group.save()
        return self

    def __str__(self):
        """ Return the string representation of the user
        related to this client.
        """
        return self.name
