from rest_framework import serializers

from logistics.serializers import AddressSerializer
from .models import Waypoint


class WaypointListSerializer(serializers.ModelSerializer):
    """ Serializer to represent a Waypoint object
        through a REST endpoint.
    """
    address = AddressSerializer()

    class Meta:
        model = Waypoint
        fields = (
            'id',
            'name',
            'latitude',
            'longitude',
            'address')

        read_only_fields = (
            'id',
            'name',
            'latitude',
            'longitude',
            'address')


class WaypointSerializer(serializers.ModelSerializer):
    """ Serializer to represent a Waypoint object
        through a REST endpoint.
    """

    address = AddressSerializer()
    entity = serializers.SerializerMethodField()
    carriers = serializers.SerializerMethodField()

    def get_entity(self, obj):
        return obj.entity.name

    def get_carriers(self, obj):
        carrier_names = [carrier.name for carrier in obj.carriers.all()]
        return carrier_names

    class Meta:
        model = Waypoint

        fields = (
            'id',
            'name',
            'entity',
            'time_open',
            'time_close',
            'lunch_break',
            'lunch_time_start',
            'lunch_time_end',
            'open_saturday',
            'saturday_time_start',
            'saturday_time_end',
            'open_holidays',
            'holiday_time_start',
            'holiday_time_end',
            'contact_name',
            'contact_last_name',
            'contact_email',
            'contact_phone',
            'contact_phone_extension',
            'address',
            'latitude',
            'longitude',
            'carriers')

        read_only_fields = (
            'id',
            'name',
            'entity',
            'time_open',
            'time_close',
            'lunch_break',
            'lunch_time_start',
            'lunch_time_end',
            'open_saturday',
            'saturday_time_start',
            'saturday_time_end',
            'open_holidays',
            'holiday_time_start',
            'holiday_time_end',
            'contact_name',
            'contact_last_name',
            'contact_email',
            'contact_phone',
            'contact_phone_extension',
            'address',
            'latitude',
            'longitude',
            'carriers')


class WaypointLiteSerializer(serializers.ModelSerializer):
    """ Serializer to represent a Waypoint object
        through a REST endpoint.
    """
    postal_code = serializers.SerializerMethodField()
    shipment_type = serializers.SerializerMethodField()

    def get_postal_code(self, obj):
        return str(obj.address.postal_code)

    def get_shipment_type(self, obj):
        type_string = 's'
        if obj.entity == 'DHL':
            type_string = 'e'
        # elif tienda
        return type_string

    class Meta:
        model = Waypoint
        fields = (
            'id',
            'latitude',
            'longitude',
            'postal_code',
            'shipment_type')

        read_only_fields = (
            'id',
            'latitude',
            'longitude',
            'postal_code',
            'shipment_type')
