from django.contrib.auth.decorators import user_passes_test, login_required
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from .forms import WaypointModelForm, DeleteWaypointForm, WaypointGroupModelForm,\
                   DeleteWaypointGroupForm, EntityModelForm, DeleteEntityForm
from .models import Waypoint, WaypointGroup, Entity
from .utils import parse_waypoints_from_csv
from logistics.models import PostalCode, Address
from logistics.forms import AddressModelForm
from user_profiles.utils import is_admin


@login_required
@user_passes_test(is_admin)
def parse_waypoints_csv(request):
    """ This view allows an admin to create a batch of waypoints from a csv.

    """
    if request.POST and request.FILES:
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            # messages.error(request,'El archivo no es un CSV')
            return HttpResponseRedirect(reverse('administration:list_waypoints'))
        if csv_file.multiple_chunks():
            # messages.error(request,
            # 'El archivo es muy grande (%.2f MB).' % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse('administration:list_waypoints'))
        file_data = csv_file.read().decode('utf-8')
        results, errors = parse_waypoints_from_csv(file_data)
        waypoints = Waypoint.objects.filter(deleted=False)
        forms = []
        context = {}
        address_form = AddressModelForm()
        address_form.fields["postal_code"].queryset = PostalCode.objects.none()
        waypoint_form = WaypointModelForm()
        forms.append(waypoint_form)
        forms.append(address_form)
        context['waypoints'] = waypoints
        context['active_modal'] = 'modal_new_waypoint'
        context['forms'] = forms
        context['error_messages'] = errors
        return render(request, 'administration/waypoint_list.html', context)
    else:
        return HttpResponseRedirect(reverse('administration:list_waypoints'))


@login_required
@user_passes_test(is_admin)
def create_waypoint(request):
    """ This view allows an admin to create a new waypoint.

    """
    if request.method == 'POST':
        address_form = AddressModelForm(request.POST)
        waypoint_form = WaypointModelForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            if waypoint_form.is_valid():
                address.save()
                waypoint = waypoint_form.save(commit=False)
                waypoint.address = address
                waypoint.save()
                return redirect('administration:list_waypoints')
        waypoints = Waypoint.objects.filter(deleted=False)
        forms = []
        context = {}
        forms.append(waypoint_form)
        forms.append(address_form)
        context['waypoints'] = waypoints
        context['active_modal'] = 'modal_new_waypoint'
        context['forms'] = forms
        return render(request, 'administration/waypoint_list.html', context)
    else:
        return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def get_form_update_waypoint(request, id_waypoint):
    """ View that is called via ajax to render the form
    to confirm the deletion of a waypoint.

    """
    if request.is_ajax() and request.method == 'GET':
        waypoint = get_object_or_404(Waypoint, pk=id_waypoint)
        update_address_form = AddressModelForm(instance=waypoint.address,
                                               initial={'id_address': waypoint.address.pk})
        update_waypoint_form = WaypointModelForm(instance=waypoint,
                                                 initial={'id_waypoint': waypoint.pk})
        update_address_form.fields["postal_code"].queryset = PostalCode.objects.none()
        update_forms = [update_waypoint_form, update_address_form]
        context = {
            'waypoint': waypoint,
            'update_forms': update_forms
        }
        return render(request, 'waypoints/form_update_waypoint.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def update_waypoint(request):
    """ This view allows an admin to create a new waypoint.

    """
    if request.method == 'POST':
        address = get_object_or_404(Address, pk=request.POST['id_user'])
        address_form = AddressModelForm(request.POST, instance=address)
        waypoint_form = WaypointModelForm(request.POST, instance=address.waypoint)
        if address_form.is_valid():
            if waypoint_form.is_valid():
                address_form.save()
                waypoint_form.save()
                return redirect('administration:list_waypoints')
        waypoints = Waypoint.objects.filter(deleted=False)
        update_forms = [address_form, waypoint_form]
        empty_address_form = AddressModelForm()
        empty_address_form.fields["postal_code"].queryset = PostalCode.objects.none()
        empty_waypoint_form = WaypointModelForm()
        empty_forms = [empty_waypoint_form, empty_address_form]
        context = {}
        context['waypoints'] = waypoints
        context['active_modal'] = 'modal_update_waypoint'
        context['forms'] = empty_forms
        context['update_forms'] = update_forms
        return render(request, 'administration/waypoint_list.html', context)
    else:
        return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def get_form_delete_waypoint(request, id_waypoint):
    """ View that is called via ajax to render the form
    to confirm the deletion of a Waypoint.

    """
    if request.is_ajax() and request.method == 'GET':
        waypoint = get_object_or_404(Waypoint, pk=id_waypoint)
        form = DeleteWaypointForm(initial={'id_waypoint': waypoint.pk})
        context = {
            'waypoint': waypoint,
            'delete_form': form
        }
        return render(request, 'waypoints/form_delete_waypoint.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def delete_waypoint(request):
    """ This view soft deletes a waypoint by setting the active attribute to false
    for the Waypoint as well as the related address instance.

    """
    if request.method == 'POST':
        form = DeleteWaypointForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('administration:list_waypoints')
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def waypoint_profile(request, id_waypoint):
    """ This view returns the entire info related to a waypoint.

    """
    if request.is_ajax() and request.method == 'GET':
        waypoint = get_object_or_404(Waypoint, pk=id_waypoint)
        address_form = AddressModelForm(instance=waypoint.address)
        waypoint_form = WaypointModelForm(instance=waypoint)
        forms = [waypoint_form, address_form]
        # print(waypoint_form)
        carriers = ', '.join([c.name for c in waypoint.carriers.all()])
        state = waypoint.address.postal_code.state
        country = state.country
        context = {
            'forms': forms,
            'carriers': carriers,
            'country': country,
            'state': state
        }
        return render(request, 'waypoints/waypoint_info.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def change_status(request):
    """ This view allows an admin to create a new waypoint.

    """
    if request.method == 'POST':
        post_data = request.POST.copy()
        entities = post_data.pop('entities')
        if 'fedex' in entities:
            Waypoint.objects.filter(entity='Fedex').update(active=True)
        else:
            Waypoint.objects.filter(entity='Fedex').update(active=False)
        if 'estafeta' in entities:
            Waypoint.objects.filter(entity='Estafeta').update(active=True)
        else:
            Waypoint.objects.filter(entity='Estafeta').update(active=False)
        if 'dhl' in entities:
            Waypoint.objects.filter(entity='DHL').update(active=True)
        else:
            Waypoint.objects.filter(entity='DHL').update(active=False)
        return redirect('administration:list_waypoints')
    else:
        return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def create_waypoint_group(request):
    """ This view allows an admin to create a new waypoint_group.

    """
    if request.method == 'POST':
        waypoint_group_form = WaypointGroupModelForm(request.POST)
        if waypoint_group_form.is_valid():
            waypoint_group_form.save()
            return redirect('administration:list_waypoint_groups')
        waypoint_groups = WaypointGroup.objects.all()
        forms = []
        context = {}
        forms.append(waypoint_group_form)
        context['groups'] = waypoint_groups
        context['active_modal'] = 'modal_new_group'
        context['forms'] = forms
        return render(request, 'administration/waypoint_group_list.html', context)
    else:
        return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def get_form_update_waypoint_group(request, id_waypoint_group):
    """ View that is called via ajax to render the form
    to confirm the deletion of a waypoint_group.

    """
    if request.is_ajax() and request.method == 'GET':
        waypoint_group = get_object_or_404(WaypointGroup, pk=id_waypoint_group)
        init_update = {'id_waypoint_group': id_waypoint_group}
        update_waypoint_group_form = WaypointGroupModelForm(instance=waypoint_group,
                                                            initial=init_update)
        update_forms = [update_waypoint_group_form]
        context = {
            'waypoint_group': waypoint_group,
            'update_forms': update_forms
        }
        return render(request, 'waypoint_groups/form_update_group.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def update_waypoint_group(request):
    """ This view allows an admin to create a new waypoint_group.

    """
    if request.method == 'POST':
        group = get_object_or_404(WaypointGroup, pk=request.POST['id_waypoint_group'])
        waypoint_group_form = WaypointGroupModelForm(request.POST, instance=group)
        if waypoint_group_form.is_valid():
            waypoint_group_form.save()
            return redirect('administration:list_waypoint_groups')
        waypoint_groups = WaypointGroup.objects.all()
        update_forms = [waypoint_group_form]
        empty_waypoint_group_form = WaypointGroupModelForm()
        empty_forms = [empty_waypoint_group_form]
        context = {}
        context['waypoint_groups'] = waypoint_groups
        context['active_modal'] = 'modal_update_group'
        context['forms'] = empty_forms
        context['update_forms'] = update_forms
        return render(request, 'administration/waypoint_group_list.html', context)
    else:
        return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def get_form_delete_waypoint_group(request, id_waypoint_group):
    """ View that is called via ajax to render the form
    to confirm the deletion of a Waypoint_group.

    """
    if request.is_ajax() and request.method == 'GET':
        waypoint_group = get_object_or_404(WaypointGroup, pk=id_waypoint_group)
        form = DeleteWaypointGroupForm(initial={'id_waypoint_group': waypoint_group.pk})
        context = {
            'group': waypoint_group,
            'delete_form': form
        }
        return render(request, 'waypoint_groups/form_delete_group.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def delete_waypoint_group(request):
    """ This view soft deletes a waypoint_group by setting the active attribute to false
    for the Waypoint_group as well as the related address instance.

    """
    if request.method == 'POST':
        form = DeleteWaypointGroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('administration:list_waypoint_groups')
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def waypoint_group_profile(request, id_waypoint_group):
    """ This view returns the entire info related to a waypoint_group.

    """
    if request.is_ajax() and request.method == 'GET':
        waypoint_group = get_object_or_404(WaypointGroup, pk=id_waypoint_group)
        waypoint_group_form = WaypointGroupModelForm(instance=waypoint_group)
        forms = [waypoint_group_form]
        e_list = ['{}'.format(e.name) for e in waypoint_group.entities.all()]
        print(e_list)
        entities_string = ', '.join(e_list)
        context = {
            'forms': forms,
            'entities': entities_string,
        }
        return render(request, 'waypoint_groups/group_info.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def create_entity(request):
    """ This view allows an admin to create a new entity.

    """
    if request.method == 'POST':
        entity_form = EntityModelForm(request.POST)
        if entity_form.is_valid():
            entity_form.save()
            return redirect('administration:list_entities')
        entities = Entity.objects.filter()
        forms = []
        context = {}
        forms.append(entity_form)
        context['entities'] = entities
        context['active_modal'] = 'modal_new_entity'
        context['forms'] = forms
        return render(request, 'administration/entity_list.html', context)
    else:
        return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def update_entity(request):
    """ This view allows an admin to create a new entity.

    """
    if request.method == 'POST':
        entity = get_object_or_404(Entity, pk=request.POST['id_entity'])
        entity_form = EntityModelForm(request.POST, instance=entity)
        if entity_form.is_valid():
            entity_form.save()
            return redirect('administration:list_entities')
        entities = Entity.objects.all()
        update_forms = [entity_form]
        empty_entity_form = EntityModelForm()
        empty_forms = [empty_entity_form]
        context = {}
        context['entities'] = entities
        context['active_modal'] = 'modal_update_entity'
        context['forms'] = empty_forms
        context['update_forms'] = update_forms
        return render(request, 'administration/entity_list.html', context)
    else:
        return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def get_form_update_entity(request, id_entity):
    """ View that is called via ajax to render the form
    to confirm the deletion of a entity.

    """
    if request.is_ajax() and request.method == 'GET':
        entity = get_object_or_404(Entity, pk=id_entity)
        init_update = {'id_entity': id_entity}
        update_entity_form = EntityModelForm(instance=entity,
                                             initial=init_update)
        update_forms = [update_entity_form]
        context = {
            'entity': entity,
            'update_forms': update_forms
        }
        return render(request, 'entities/form_update_entity.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def get_form_delete_entity(request, id_entity):
    """ View that is called via ajax to render the form
    to confirm the deletion of a entity.

    """
    if request.is_ajax() and request.method == 'GET':
        entity = get_object_or_404(Entity, pk=id_entity)
        form = DeleteEntityForm(initial={'id_entity': entity.pk})
        context = {
            'entity': entity,
            'delete_form': form
        }
        return render(request, 'entities/form_delete_entity.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def delete_entity(request):
    """ This view soft deletes a entity by setting the active attribute to false
    for the entity as well as the related address instance.

    """
    if request.method == 'POST':
        form = DeleteEntityForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('administration:list_entities')
    return HttpResponseBadRequest()
