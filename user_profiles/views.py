from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UserModelForm, ClientModelForm, DeleteClientForm
from .models import Client
from .utils import is_admin


@login_required
@user_passes_test(is_admin)
def create_client(request):
    """ This view allows an admin to create a new client.

    """
    if request.method == 'POST':
        user_form = UserModelForm(request.POST)
        client_form = ClientModelForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            if client_form.is_valid():
                user.save()
                client_form.save(form_user=user)
                return redirect('administration:list_clients')
        clients = Client.objects.filter(active=True)
        forms = []
        context = {}
        forms.append(user_form)
        forms.append(client_form)
        context['clients'] = clients
        context['active_modal'] = 'modal_new_client'
        context['forms'] = forms
        return render(request, 'administration/client_list.html', context)
    else:
        return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def get_form_update_client(request, id_client):
    """ View that is called via ajax to render the form
    to confirm the deletion of a Client.

    """
    if request.is_ajax() and request.method == 'GET':
        client = get_object_or_404(Client, pk=id_client)
        update_user_form = UserModelForm(instance=client.user,
                                         initial={'id_user': client.user.pk})
        update_client_form = ClientModelForm(instance=client)
        update_forms = [update_user_form, update_client_form]
        context = {
            'client': client,
            'update_forms': update_forms
        }
        return render(request, 'user_profiles/form_update_client.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def update_client(request):
    """ This view allows an admin to create a new client.

    """
    if request.method == 'POST':
        user = get_object_or_404(get_user_model(), pk=request.POST['id_user'])
        user_form = UserModelForm(request.POST, instance=user)
        client_form = ClientModelForm(request.POST, instance=user.client)
        if user_form.is_valid():
            if client_form.is_valid():
                user_form.save()
                client_form.save()
                return redirect('administration:list_clients')
        clients = Client.objects.filter(active=True)
        update_forms = [user_form, client_form]
        empty_user_form = UserModelForm()
        empty_client_form = ClientModelForm()
        empty_forms = [empty_user_form, empty_client_form]
        context = {}
        context['clients'] = clients
        context['active_modal'] = 'modal_update_client'
        context['forms'] = empty_forms
        context['update_forms'] = update_forms
        return render(request, 'administration/client_list.html', context)
    else:
        return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def get_form_delete_client(request, id_client):
    """ View that is called via ajax to render the form
    to confirm the deletion of a Client.

    """
    if request.is_ajax() and request.method == 'GET':
        client = get_object_or_404(Client, pk=id_client)
        form = DeleteClientForm(initial={'id_client': client.pk})
        context = {
            'client': client,
            'delete_form': form
        }
        return render(request, 'user_profiles/form_delete_client.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def delete_client(request):
    """ This view soft deletes a client by setting the active attribute to false
    for the Client as well as the related user instance.

    """
    if request.method == 'POST':
        form = DeleteClientForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('administration:list_clients')
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_admin)
def client_profile(request, id_client):
    """ This view returns the entire info related to a client.

    """
    if request.is_ajax() and request.method == 'GET':
        client = get_object_or_404(Client, pk=id_client)
        user_form = UserModelForm(instance=client.user)
        client_form = ClientModelForm(instance=client)
        groups = ', '.join([g.name for g in client.groups.all()])
        forms = [user_form, client_form]
        context = {
            'forms': forms,
            'groups': groups
        }
        return render(request, 'user_profiles/client_info.html', context)
    return HttpResponseBadRequest()
