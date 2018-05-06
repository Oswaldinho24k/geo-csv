import os
import time
import uuid
from django.db import models
from fedex_wrapper import waybill_generation
from estafeta_wrapper import shipping
from core.utils import normalize_string, is_production, store_pdf
from core.validators import PHONE_REGEX


# Create your models here.
class Carrier(models.Model):
    """
    """

    name = models.CharField(max_length=35,
                            blank=False,
                            verbose_name='Nombre del Transportista')

    def __str__(self):
        """ Return the string representation of the address.
        """

        return self.name


class Country(models.Model):
    """
    """

    name = models.CharField(max_length=35,
                            blank=False,
                            verbose_name='Pais')
    code = models.CharField(max_length=2,
                            blank=False,
                            verbose_name='Codigo de Pais')

    def __str__(self):
        """ Return the string representation of the address.
        """

        return self.name


class State(models.Model):
    """
    """

    name = models.CharField(max_length=35,
                            blank=False,
                            verbose_name='Estado')
    code = models.CharField(max_length=2,
                            blank=False,
                            verbose_name='Codigo de Estado (2 letras)')
    country = models.ForeignKey('logistics.Country')

    def __str__(self):
        """ Return the string representation of the address.
        """

        return self.name


class PostalCode(models.Model):
    """
    """

    state = models.ForeignKey('logistics.State')

    code = models.CharField(max_length=5,
                            blank=False,
                            verbose_name='Código Postal')
    latitude = models.DecimalField(max_digits=25,
                                   decimal_places=22,
                                   blank=True,
                                   verbose_name='Latitud')
    longitude = models.DecimalField(max_digits=25,
                                    decimal_places=22,
                                    blank=True,
                                    verbose_name='Longitud')

    def __str__(self):
        """ Return the string representation of the address.
        """

        return self.code


class Address(models.Model):
    """
    """

    city = models.CharField(max_length=35,
                            blank=False,
                            verbose_name='Municipio/Delegación')
    line_one = models.CharField(max_length=35,
                                blank=False,
                                verbose_name='Dirección 1')
    line_two = models.CharField(max_length=35,
                                blank=True,
                                verbose_name='Dirección 2')
    neighborhood = models.CharField(max_length=35,
                                    blank=True,
                                    verbose_name='Colonia')
    postal_code = models.ForeignKey('logistics.PostalCode')

    def __str__(self):
        """ Return the string representation of the address.
        """

        address_string = '{line_one}, {line_two}, C.P. {postal_code}'
        return address_string.format(line_one=self.line_one,
                                     line_two=self.line_two,
                                     postal_code=self.postal_code)

    def fedex_dict(self):
        address_dictionary = {'StreetLines': [normalize_string(self.line_one),
                                              normalize_string(self.line_two)],
                              'City': normalize_string(self.city),
                              'StateOrProvinceCode': normalize_string(self.postal_code.state.code),
                              'PostalCode': self.postal_code.code,
                              'CountryCode': self.postal_code.state.country.code,
                              'CountryName': normalize_string(self.postal_code.state.country.name),
                              'Residential': False}

        return address_dictionary

    def estafeta_dict(self):
        address_dictionary = {
            'address1': normalize_string(self.line_one),
            'address2': normalize_string(self.line_two),
            'city': normalize_string(self.city),
            'neighborhood': normalize_string(self.neighborhood),
            'state': normalize_string(self.postal_code.state.name),
            'zipCode': self.postal_code.code
        }

        if len(address_dictionary['address2']) <= 0:
            address_dictionary['address2'] = '-'
        if len(address_dictionary['neighborhood']) <= 0:
            address_dictionary['neighborhood'] = '-'
        return address_dictionary


class Contact(models.Model):
    """ Class for storing the information of contacts for the shipments

    """
    person_name = models.CharField(max_length=255)
    title = models.CharField(max_length=250,
                             blank=True)
    company_name = models.CharField(max_length=500,
                                    blank=True)
    phone_number = models.CharField(max_length=16,
                                    validators=[PHONE_REGEX],
                                    blank=True)
    phone_extension = models.CharField(max_length=8,
                                       blank=True)
    email_address = models.EmailField(blank=True)

    def fedex_dict(self):
        contact_dictionary = {'PersonName': self.person_name,
                              'CompanyName': self.company_name,
                              'PhoneNumber': self.phone_number,
                              'PhoneExtension': self.phone_extension,
                              'EMailAddress': self.email_address}

        return contact_dictionary

    def estafeta_dict(self):
        contact_dictionary = {
            'cellPhone': self.phone_number,
            'contactName': self.person_name,
            'corporateName': self.company_name
        }

        return contact_dictionary


class Shipment(models.Model):
    """ Class for storing all of the shipments generated by the system.

    """
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    client = models.ForeignKey('user_profiles.Client', null=True)
    shipper_address = models.ForeignKey('logistics.Address',
                                        related_name='shipper_address',
                                        null=True)
    shipper_contact = models.ForeignKey('logistics.Contact',
                                        related_name='shipper_contact',
                                        null=True)
    recipient_address = models.ForeignKey('logistics.Address',
                                          related_name='recipient_address',
                                          null=True)
    recipient_contact = models.ForeignKey('logistics.Contact',
                                          related_name='recipient_contact',
                                          null=True)
    carrier = models.ForeignKey('logistics.Carrier', null=True)
    waypoint = models.ForeignKey('waypoints.Waypoint', null=True, blank=True)
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    weight = models.FloatField()
    tracking_number = models.CharField(max_length=255,
                                       blank=True)
    waybill_link = models.URLField(max_length=500,
                                   blank=True)
    third_party_reference = models.CharField(max_length=35,
                                             blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ Print a waybill

        """
        waybill_string = '{tracking_number}'
        return waybill_string.format(tracking_number=self.tracking_number)

    def get_reference(self):
        if len(self.third_party_reference) > 0:
            return self.third_party_reference
        return 'Sin referencia'

    def create_fedex_waybill(self):
        """
        Create a new waybill with fedex.
        """
        return waybill_generation.ship(
            production=is_production(),
            key=os.environ['FEDEX_KEY'],
            password=os.environ['FEDEX_PASSWORD'],
            account_number=os.environ['FEDEX_ACCOUNT_NUMBER'],
            meter_number=os.environ['FEDEX_METER_NUMBER'],
            shipper_address=self.shipper_address.fedex_dict(),
            shipper_contact=self.shipper_contact.fedex_dict(),
            recipient_address=self.recipient_address.fedex_dict(),
            recipient_contact=self.recipient_contact.fedex_dict(),
            length=self.length,
            width=self.width,
            height=self.height,
            weight=self.weight,
            customer_reference_value=self.client.id,
            order_reference_value=self.third_party_reference
        )

    def create_estafeta_waybill(self):
        """
        Create a waybill with estafeta.
        """
        return shipping.ship(
            production=is_production(),
            login=os.environ['ESTAFETA_SHIP_LOGIN'],
            password=os.environ['ESTAFETA_SHIP_PASSWORD'],
            subscriber_id=os.environ['ESTAFETA_SHIP_SUBSCRIBER'],
            customer_number=os.environ['ESTAFETA_SHIP_CUSTOMER'],
            office_number=os.environ['ESTAFETA_SHIP_OFFICE'],
            service_type=os.environ['ESTAFETA_SHIP_SERVICE'],
            d_info={**(self.recipient_address.estafeta_dict()),
                    **(self.recipient_contact.estafeta_dict())},
            o_info={**(self.shipper_address.estafeta_dict()),
                    **(self.shipper_contact.estafeta_dict())},
            weight=self.weight,
            content='Paquete',
            additional_info='Cliente: ' + str(self.client.id),
            reference=self.get_reference()
        )

    def log_waybill_errors(self, waybill, carrier):
        """ Saves the errors from a waybill request.
        """
        error_file_name = carrier + time.strftime("%Y-%m-%d-%H:%M:%S") + '.txt'
        estafeta_error_path = '/tmp/' + error_file_name
        with open(estafeta_error_path, 'w+') as error:
            error.write(str(waybill))

    def create_waybill(self):
        """
        This method allows for the creation of a waybill, from
        the information already stored on an instance of this model.
        """
        try:
            if self.carrier.name == 'Fedex':
                waybill = self.create_fedex_waybill()
                self.log_waybill_errors(waybill, 'fedex')
                shipment_detail = waybill.CompletedShipmentDetail
                completed_package_details = shipment_detail.CompletedPackageDetails[0]
                self.tracking_number = completed_package_details.TrackingIds[0].TrackingNumber
                binary_label_data = completed_package_details.Label.Parts[0].Image
            elif self.carrier.name == 'Estafeta':
                waybill = self.create_estafeta_waybill()
                self.log_waybill_errors(waybill, 'estafeta')
                self.tracking_number = waybill.labelResultList[0].resultDescription
                binary_label_data = waybill.labelPDF

            self.waybill_link = store_pdf(binary_label_data)
        except Exception as e:
            return False

        return True


class ExternalShipment(models.Model):
    """ Class for storing the external shipments confirmed by the client.

    """
    client = models.ForeignKey('user_profiles.Client', null=True)
    waypoint = models.ForeignKey('waypoints.Waypoint')
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=50,
                                verbose_name='Numero de Orden del Cliente')

    def __str__(self):
        """ Return the string representation of the address.
        """
        date_string = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return '{} | ID: {}'.format(date_string, self.unique_id)
