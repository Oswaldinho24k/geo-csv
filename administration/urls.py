from django.conf.urls import url
from .views import list_clients, list_waypoints, list_waypoint_groups, main_dashboard, \
                   list_shipments_api, list_shipments_external, list_entities
app_name = 'administration'

urlpatterns = [
    url(r'^list_clients/$', list_clients, name='list_clients'),
    url(r'^list_entities/$', list_entities, name='list_entities'),
    url(r'^list_waypoints/$', list_waypoints, name='list_waypoints'),
    url(r'^list_groups/$', list_waypoint_groups, name='list_waypoint_groups'),
    url(r'^list_shipments_api/$', list_shipments_api, name='list_shipments_api'),
    url(r'^list_shipments_external/$', list_shipments_external, name='list_shipments_external'),
    url(r'^dashboard/$', main_dashboard, name='main_dashboard'),
]
