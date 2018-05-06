from django.conf.urls import url
from .views import create_waypoint, delete_waypoint, get_form_delete_waypoint, \
                   update_waypoint, get_form_update_waypoint, waypoint_profile, \
                   parse_waypoints_csv, change_status, create_waypoint_group, \
                   get_form_update_waypoint_group, update_waypoint_group, \
                   get_form_delete_waypoint_group, delete_waypoint_group, \
                   waypoint_group_profile, create_entity, update_entity, \
                   get_form_update_entity, get_form_delete_entity, delete_entity

app_name = 'waypoints'

urlpatterns = [
    url(r'^parse_csv/$', parse_waypoints_csv, name='parse_csv'),
    url(r'^create_waypoint/$', create_waypoint, name='create_waypoint'),
    url(r'^change-status/$', change_status, name='change_status'),
    url(r'^form_update_waypoint/(?P<id_waypoint>[0-9]+)$',
        get_form_update_waypoint,
        name='form_update_waypoint'),
    url(r'^update_waypoint/$', update_waypoint, name='update_waypoint'),
    url(r'^form_delete_waypoint/(?P<id_waypoint>[0-9]+)$',
        get_form_delete_waypoint,
        name='form_delete_waypoint'),
    url(r'^delete_waypoint/$', delete_waypoint, name='delete_waypoint'),
    url(r'^waypoint_profile/(?P<id_waypoint>[0-9]+)$',
        waypoint_profile,
        name='waypoint_profile'),
    url(r'^create_waypoint_group/$', create_waypoint_group, name='create_waypoint_group'),
    url(r'^form_update_waypoint_group/(?P<id_waypoint_group>[0-9]+)$',
        get_form_update_waypoint_group,
        name='form_update_waypoint_group'),
    url(r'^update_waypoint_group/$', update_waypoint_group, name='update_waypoint_group'),
    url(r'^form_delete_waypoint_group/(?P<id_waypoint_group>[0-9]+)$',
        get_form_delete_waypoint_group,
        name='form_delete_waypoint_group'),
    url(r'^delete_waypoint_group/$', delete_waypoint_group, name='delete_waypoint_group'),
    url(r'^waypoint_group_profile/(?P<id_waypoint_group>[0-9]+)$',
        waypoint_group_profile,
        name='waypoint_group_profile'),
    url(r'^create_entity/$', create_entity, name='create_entity'),
    url(r'^form_update_entity/(?P<id_entity>[0-9]+)$',
        get_form_update_entity,
        name='form_update_entity'),
    url(r'^update_entity/$', update_entity, name='update_entity'),
    url(r'^form_delete_entity/(?P<id_entity>[0-9]+)$',
        get_form_delete_entity,
        name='form_delete_entity'),
    url(r'^delete_entity/$', delete_entity, name='delete_entity'),
]
