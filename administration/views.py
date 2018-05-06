from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from django.core.cache import cache
from user_profiles.forms import UserModelForm, ClientModelForm
from user_profiles.models import Client
from user_profiles.utils import is_admin
from logistics.models import PostalCode, Shipment, ExternalShipment
from logistics.forms import AddressModelForm
from waypoints.forms import WaypointModelForm, WaypointGroupModelForm, EntityModelForm
from waypoints.models import Waypoint, WaypointGroup, Entity
from core.utils import get_environment, get_hardware_information


@login_required
@user_passes_test(is_admin)
def list_clients(request):
    """ This view allows an admin to have a full
    view of the clients on the platform.
    """
    clients = Client.objects.filter(active=True)
    user_form = UserModelForm()
    client_form = ClientModelForm()
    forms = [user_form, client_form]
    context = {}
    context['clients'] = clients
    context['forms'] = forms
    context['page_title'] = 'Clientes'
    context['env'] = get_environment()
    return render(request, 'administration/client_list.html', context)


@login_required
@user_passes_test(is_admin)
def list_entities(request):
    """ This view allows an admin to have a full
    view of the entities on the platform.
    """
    entities = Entity.objects.all()
    for e in entities:
        e.waypoint_count = e.waypoint_set.filter(active=True).count()
    entity_form = EntityModelForm()
    forms = [entity_form]
    context = {}
    context['entities'] = entities
    context['forms'] = forms
    context['page_title'] = 'Entidades'
    context['env'] = get_environment()
    return render(request, 'administration/entity_list.html', context)


@login_required
@user_passes_test(is_admin)
def list_waypoints(request):
    """ This view allows an admin to have a full
    view of the waypoints on the platform.
    """
    waypoints = cache.get('waypoints_all')
    if waypoints is None:
        waypoints = list(Waypoint.objects.filter(deleted=False))
        cache.set('waypoints_all', waypoints)
    address_form = AddressModelForm()
    # Pulling this with JS
    address_form.fields["postal_code"].queryset = PostalCode.objects.none()
    waypoint_form = WaypointModelForm()
    forms = [waypoint_form, address_form]
    context = {}
    context['waypoints'] = waypoints
    context['forms'] = forms
    context['page_title'] = 'Puntos'
    context['env'] = get_environment()
    return render(request, 'administration/waypoint_list.html', context)


@login_required
@user_passes_test(is_admin)
def list_shipments_api(request):
    """ This view allows an admin to have a full
    view of the shipments from the API on the platform.
    """
    shipments = Shipment.objects.order_by('-created_at')
    context = {}
    context['shipments'] = shipments
    context['page_title'] = 'Envios API'
    context['env'] = get_environment()
    return render(request, 'administration/shipment_api_list.html', context)


@login_required
@user_passes_test(is_admin)
def list_shipments_external(request):
    """ This view allows an admin to have a full
    view of the shipments from other sources on the platform.
    """
    shipments = ExternalShipment.objects.order_by('-created_at')
    context = {}
    context['shipments'] = shipments
    context['page_title'] = 'Envios Externos'
    context['env'] = get_environment()
    return render(request, 'administration/shipment_external_list.html', context)


@login_required
@user_passes_test(is_admin)
def list_waypoint_groups(request):
    """ This view allows an admin to have a full
    view of the waypoints on the platform.
    """
    waypoint_groups = WaypointGroup.objects.all()
    entities_dict = {}
    for group in waypoint_groups:
        total = 0
        for entity in group.entities.all():
            if entity.name not in entities_dict.keys():
                entities_dict[entity.name] = entity.waypoint_set.filter(deleted=False).count()
            total += entities_dict[entity.name]
        group.waypoints_length = total
    waypoint_group_form = WaypointGroupModelForm()
    forms = [waypoint_group_form]
    context = {}
    context['groups'] = waypoint_groups
    context['forms'] = forms
    context['page_title'] = 'Grupos'
    context['env'] = get_environment()
    return render(request, 'administration/waypoint_group_list.html', context)


@login_required
@user_passes_test(is_admin)
def main_dashboard(request):
    """ This view allows an admin to have a full
    view of the clients on the platform.
    """
    shipment_count = Shipment.objects.count()
    context = {}
    context['shipment_count'] = shipment_count
    server = get_hardware_information()
    context['cpu_percent'] = server['cpu_percent']
    context['ram_percent'] = server['ram_percent']

    context['page_title'] = 'Dashboard'
    context['env'] = get_environment()
    return render(request, 'administration/main_dashboard.html', context)
