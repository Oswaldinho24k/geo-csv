from rest_framework import serializers
from waypoints.models import Waypoint
from .models import Carrier, PostalCode, Address, Contact, Shipment, ExternalShipment
from .models import State


class StateSerializer(serializers.ModelSerializer):
    """
    Serializer that allows you to get the details of a given state.
    """
    class Meta:
        model = State
        fields = (
            'name',
            'code', 
        )

        # read_only_fields = (
        #     'name',
        #     'code', 
        # )


class PostalCodeSerializer(serializers.ModelSerializer):
    """
    Serializer that allows you to get all the details of a given
    postal code.
    """

    state = StateSerializer()

    class Meta:
        model = PostalCode
        fields = (
            'state',
            'code',
            'latitude',
            'longitude', 
        )

        # read_only_fields = (
        #     'state',
        #     'code',
        #     'latitude',
        #     'longitude', 
        # )


class AddressSerializer(serializers.ModelSerializer):

    postal_code = PostalCodeSerializer()

    class Meta:
        model = Address
        fields = ('city',
                  'line_one',
                  'line_two',
                  'postal_code', )

    def create(self, validated_data):
        postal_code = validated_data.pop('postal_code')
        postal_code_object = PostalCode.objects.filter(code=postal_code.get('code')).get()
        validated_data['postal_code'] = postal_code_object
        address = Address.objects.create(city=validated_data['city'],
                                         line_one=validated_data['line_one'],
                                         line_two=validated_data['line_two'],
                                         postal_code=validated_data['postal_code'])
        return address


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('person_name',
                  'title',
                  'company_name',
                  'phone_number',
                  'phone_extension',
                  'email_address', )
        extra_kwargs = {'title': {'required': False},
                        'company_name': {'required': False},
                        'phone_number': {'required': False},
                        'phone_extension': {'required': False}}


class ShipmentSerializer(serializers.ModelSerializer):
    
    shipper_address = AddressSerializer()
    shipper_contact = ContactSerializer()
    recipient_address = AddressSerializer()
    recipient_contact = ContactSerializer()

    class Meta:
        model = Shipment
        fields = ('waypoint',
                  'shipper_address',
                  'shipper_contact',
                  'recipient_address',
                  'recipient_contact',
                  'length',
                  'width',
                  'height',
                  'weight',
                  'third_party_reference', )

    def create(self, validated_data):
        client = self.context['request'].user.client
        s_address_data = validated_data.pop('shipper_address')
        postal_code = s_address_data.pop('postal_code')
        postal_code_object = PostalCode.objects.filter(code=postal_code.get('code')).get()
        s_address_data['postal_code'] = postal_code_object
        s_address = Address.objects.create(**s_address_data)
        s_contact_data = validated_data.pop('shipper_contact')
        s_contact = Contact.objects.create(**s_contact_data)
        if 'waypoint' in validated_data and validated_data['waypoint']:
            waypoint = validated_data.pop('waypoint')
            waypoint = Waypoint.objects.get(pk=waypoint.id)
            carrier = waypoint.carriers.get()
            r_address = waypoint.address
            validated_data.pop('recipient_address')

        else:
            if 'waypoint' in validated_data:
                validated_data.pop('waypoint')
            waypoint = None
            r_address_data = validated_data.pop('recipient_address')
            postal_code = r_address_data.pop('postal_code')
            postal_code_object = PostalCode.objects.filter(code=postal_code.get('code')).get()
            carrier = Carrier.objects.get(name='Fedex')
            r_address_data['postal_code'] = postal_code_object
            r_address = Address.objects.create(**r_address_data)

        r_contact_data = validated_data.pop('recipient_contact')
        r_contact = Contact.objects.create(**r_contact_data)
        shipment = Shipment.objects.create(client=client,
                                           waypoint=waypoint,
                                           shipper_address=s_address,
                                           shipper_contact=s_contact,
                                           recipient_address=r_address,
                                           recipient_contact=r_contact,
                                           carrier=carrier,
                                           **validated_data)

        return shipment


class InitialShipmentSerializer(serializers.ModelSerializer):
    """
    Serializer that allows you to create a new Shipment
    In order to return the token to the user.
    """
    class Meta:
        model = Shipment
        fields = ('length',
                  'width',
                  'height',
                  'weight', )

    def create(self, validated_data):
        client = self.context['request'].user.client
        shipment = Shipment.objects.create(client=client,
                                           **validated_data)
        return shipment


class FillInformationSerializer(serializers.ModelSerializer):
    """
    Serializer that allows the fullfillment of all the client
    information in another step.
    """
    shipper_address = AddressSerializer()
    shipper_contact = ContactSerializer()
    recipient_address = AddressSerializer()
    recipient_contact = ContactSerializer()

    class Meta:
        model = Shipment
        fields = ('waypoint',
                  'shipper_address',
                  'shipper_contact',
                  'recipient_address',
                  'recipient_contact',
                  'third_party_reference', )

    def update(self, instance, validated_data):
        s_address_data = validated_data.pop('shipper_address')
        postal_code = s_address_data.pop('postal_code')
        postal_code_object = PostalCode.objects.filter(code=postal_code.get('code')).get()
        s_address_data['postal_code'] = postal_code_object
        s_address = Address.objects.create(**s_address_data)
        s_contact_data = validated_data.pop('shipper_contact')
        s_contact = Contact.objects.create(**s_contact_data)

        if 'waypoint' in validated_data and validated_data['waypoint']:
            waypoint = validated_data.pop('waypoint')
            waypoint = Waypoint.objects.get(pk=waypoint.id)
            carrier = waypoint.carriers.get()
            r_address = waypoint.address
            validated_data.pop('recipient_address')
        else:
            if 'waypoint' in validated_data:
                validated_data.pop('waypoint')
            waypoint = None
            r_address_data = validated_data.pop('recipient_address')
            postal_code = r_address_data.pop('postal_code')
            postal_code_object = PostalCode.objects.filter(code=postal_code.get('code')).get()
            carrier = Carrier.objects.get(name='Fedex')
            r_address_data['postal_code'] = postal_code_object
            r_address = Address.objects.create(**r_address_data)

        r_contact_data = validated_data.pop('recipient_contact')
        r_contact = Contact.objects.create(**r_contact_data)

        instance.waypoint = waypoint
        instance.shipper_address = s_address
        instance.shipper_contact = s_contact
        instance.recipient_address = r_address
        instance.recipient_contact = r_contact
        instance.carrier = carrier
        
        third_party_reference = validated_data.get('third_party_reference', '')
        instance.third_party_reference = third_party_reference
        instance.save()

        return instance


class ExternalShipmentSerializer(serializers.ModelSerializer):
    """
    Serializer that allows you to create a new Shipment
    In order to return the token to the user.
    """
    class Meta:
        model = ExternalShipment
        fields = ('waypoint',
                  'order_id',
                  'client', )

    def create(self, validated_data):
        client = self.context['request'].user.client
        external_shipment = ExternalShipment.objects.create(client=client,
                                                            **validated_data)
        return external_shipment
