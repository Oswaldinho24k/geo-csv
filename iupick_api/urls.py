from django.conf.urls import url, include
from waypoints.api_views import APIWaypointInformation, APIWaypointsLite, APIPostalWaypointIds
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from logistics.api_views import create_waybill, track_shipment, \
                                create_shipment_token, fill_shipment_information, \
                                generate_waybill, confirm_waypoint_shipment, \
                                postal_code_info

from tosp_auth.api_views import ResetAuthToken

app_name = 'iupick_api'

router = DefaultRouter()
router.register(r'waypoints/lite', APIWaypointsLite, base_name='waypoints_lite')
router.register(r'waypoints/postal-ids', APIPostalWaypointIds, base_name='postal_client_ids')
router.register(r'waypoints', APIWaypointInformation, base_name='waypoints')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/$', obtain_auth_token),
    url(r'^reset-token/$', ResetAuthToken.as_view(), name='reset_auth_token'),
    url(r'^create-waybill/$', create_waybill),
    url(r'^track-shipment/$', track_shipment),
    url(r'^create-shipment-token/$', create_shipment_token),
    url(r'^waypoint-confirmation/$', confirm_waypoint_shipment),
    url(r'^fill-shipment-information/(?P<shipment_token>[0-9a-f-]+)/$',
        fill_shipment_information),
    url(r'^generate-waybill/(?P<shipment_token>[0-9a-f-]+)/$',
        generate_waybill),
    url(r'^postal_code/(?P<code>[0-9]{5})/$',
        postal_code_info)
]
