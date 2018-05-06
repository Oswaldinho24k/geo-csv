""" Utility functions and constants that will be used in the project.
"""
from django.core.exceptions import ObjectDoesNotExist
from logistics.forms import AddressModelForm
from logistics.models import Address, Carrier, Country, State, PostalCode
from .forms import WaypointModelForm
from .models import Waypoint, Entity

INVALID_STRINGS = ['', ' ', ':']


def split_phone(phone):
    extension = ''
    phone_number = phone
    if '/' in phone:
        num = phone.split('/')
        phone_number = num[0]
        extension = num[1]
    return phone_number, extension


def get_waypoints_for_groups(groups, query):
    waypoint_ids = []
    waypoints = []
    for group in groups:
        for entity in group.entities.all():
            for waypoint in entity.waypoint_set.filter(**query):
                if waypoint.pk not in waypoint_ids:
                    waypoint_ids.append(waypoint.pk)
                    waypoints.append(waypoint)
    return waypoints


def get_postal_code_address_list(postal_code):
    addresses = Address.objects.filter(postal_code=postal_code.id)
    address_list = []
    for address in addresses:
        address_list.append(address)
    return address_list


def parse_waypoints_from_csv(csv_file_data):
    """ This method parses the input csv file with 25 columns into
        the waypoint model and creates them.
    """
    errors = []
    results = []
    lines = csv_file_data.split("\n")
    row_size = len(lines[0].split(','))
    if row_size != 25:
        errors.append('Error Archivo Invalido')
        return results, errors
    waypoint_dict = {}
    address_dict = {}
    waypoints = []
    addresses = []
    carriers = []
    states_query = State.objects.all()
    carrier_query = Carrier.objects.all()
    entity_query = Entity.objects.all()
    entity_dict = {entity.name: entity for entity in entity_query}
    states_dict = {state.name: state for state in states_query}
    carrier_dict = {carrier.name: carrier for carrier in carrier_query}
    mexico = Country.objects.get(name='México')
    for i, line in enumerate(lines):
        # Check for empty lines
        if not line:
            continue
        data = line.split(',')
        # Check for headers
        if data[0] == 'name':
            continue
        waypoint_dict['name'] = data[0]
        waypoint_dict['entity'] = data[1]
        address_dict['line_one'] = data[2]
        address_dict['line_two'] = data[3]
        address_dict['neighborhood'] = data[4]
        address_dict['city'] = data[5]
        waypoint_dict['state'] = data[6]
        waypoint_dict['country'] = mexico.id
        address_dict['postal_code'] = data[7]
        if data[8] in INVALID_STRINGS or data[9] in INVALID_STRINGS:
            error = 'No es un horario valido, linea {l}'.format(l=str(i + 1))
            errors.append(error)
        else:
            waypoint_dict['time_open'] = data[8]
            waypoint_dict['time_close'] = data[9]
        if data[10] in INVALID_STRINGS or data[11] in INVALID_STRINGS:
            waypoint_dict['lunch_break'] = False
        else:
            waypoint_dict['lunch_break'] = True
            waypoint_dict['lunch_time_start'] = data[10]
            waypoint_dict['lunch_time_end'] = data[11]
        if data[12] in INVALID_STRINGS or data[13] in INVALID_STRINGS:
            waypoint_dict['open_saturday'] = False
        else:
            waypoint_dict['open_saturday'] = True
            waypoint_dict['saturday_time_start'] = data[12]
            waypoint_dict['saturday_time_end'] = data[13]
        if data[14] in INVALID_STRINGS or data[15] in INVALID_STRINGS:
            waypoint_dict['open_holidays'] = False
        else:
            waypoint_dict['open_holidays'] = True
            waypoint_dict['holiday_time_start'] = data[14]
            waypoint_dict['holiday_time_end'] = data[15]
        waypoint_dict['contact_email'] = data[16]
        waypoint_dict['contact_phone'] = data[17]
        waypoint_dict['contact_phone_extension'] = data[18]
        waypoint_dict['contact_name'] = data[19]
        waypoint_dict['contact_last_name'] = data[20]
        waypoint_dict['latitude'] = data[21]
        waypoint_dict['longitude'] = data[22]
        waypoint_dict['carriers'] = data[23].replace('\r', '')
        waypoint_dict['external_id'] = data[24]
        waypoint_dict['active'] = True
        try:
            postal_code = PostalCode.objects.get(code=address_dict['postal_code'])
            address_dict['postal_code'] = postal_code.id
        except Exception as e:
            error = '{pc} no es un codigo postal valido, linea {l}'
            error = error.format(pc=str(address_dict['postal_code']),
                                 l=str(i + 1))
            errors.append(error)
        if waypoint_dict['state'] == 'Nuevo León':
            waypoint_dict['state'] = 'Nuevo Leon'
        waypoint_dict['entity'] = entity_dict[waypoint_dict['entity']].id
        waypoint_dict['state'] = states_dict[waypoint_dict['state']].id
        cariers = [carrier_dict[waypoint_dict['carriers']].id]
        waypoint_dict['carriers'] = cariers
        waypoints.append(waypoint_dict)
        addresses.append(address_dict)
        carriers.append(cariers)
        waypoint_dict = {}
        address_dict = {}
    if errors:
        return results, errors
    for address, waypoint, carrier in zip(addresses, waypoints, carriers):
        address_form = AddressModelForm(address)
        waypoint['carriers'] = []
        w, update = None, False
        try:
            w = Waypoint.objects.get(external_id=waypoint['external_id'])
            update = True
        except ObjectDoesNotExist:
            w, update = None, False
        if update:
            w.name = waypoint['name']
            w.address.line_one = address['line_one']
            w.address.line_two = address['line_two']
            w.address.neighborhood = address['neighborhood']
            w.address.city = address['city']
            w.time_open = waypoint['time_open']
            w.time_close = waypoint['time_close']
            if waypoint['lunch_break']:
                w.lunch_time_start = waypoint['lunch_time_start']
                w.lunch_time_end = waypoint['lunch_time_end']
            if waypoint['open_saturday']:
                w.saturday_time_start = waypoint['saturday_time_start']
                w.saturday_time_end = waypoint['saturday_time_end']
            if waypoint['open_holidays']:
                w.holiday_time_start = waypoint['holiday_time_start']
                w.holiday_time_end = waypoint['holiday_time_end']
            w.contact_email = waypoint['contact_email']
            w.contact_phone = waypoint['contact_phone']
            w.contact_phone_extension = waypoint['contact_phone_extension']
            w.contact_name = waypoint['contact_name']
            w.contact_last_name = waypoint['contact_last_name']
            w.latitude = waypoint['latitude']
            w.longitude = waypoint['longitude']
            # TODO UPDATE CARRIERS
            w.address.save()
            w.save()
        else:
            waypoint_form = WaypointModelForm(waypoint)
            if waypoint_form.errors:
                print(waypoint_form.errors)
            if address_form.errors:
                print(address_form.errors)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                if waypoint_form.is_valid():
                    address.save()
                    waypoint = waypoint_form.save(commit=False)
                    waypoint.address = address
                    waypoint.save()
                    for c in carrier:
                        waypoint.carriers.add(c)
    return results, errors
