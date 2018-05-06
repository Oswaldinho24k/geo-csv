from django.conf.urls import url
from .views import create_client, delete_client, get_form_delete_client, \
                   update_client, get_form_update_client, client_profile

app_name = 'user_profiles'

urlpatterns = [
    url(r'^create_client/$', create_client, name='create_client'),
    url(r'^form_update_client/(?P<id_client>[0-9]+)$',
        get_form_update_client,
        name='form_update_client'),
    url(r'^update_client/$', update_client, name='update_client'),
    url(r'^form_delete_client/(?P<id_client>[0-9]+)$',
        get_form_delete_client,
        name='form_delete_client'),
    url(r'^delete_client/$', delete_client, name='delete_client'),
    url(r'^client_profile/(?P<id_client>[0-9]+)$',
        client_profile,
        name='client_profile'),
]
