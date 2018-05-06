from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from logistics.models import PostalCode
from .models import Waypoint
from .serializers import WaypointSerializer, WaypointListSerializer, WaypointLiteSerializer
from .utils import get_waypoints_for_groups, get_postal_code_address_list


class APIWaypointInformation(ReadOnlyModelViewSet):
    """ API to get all information for our waypoints.

        This view is a REST endpoint for developers to get all the iuPick waypoints available for
        delivery.

        Retrieves all objects from database.

        Returns
        --------

        Returns a JSON object with the id, name and coordinates of a waypoint.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WaypointSerializer
    query = {'deleted': False, 'active': True}
    queryset = Waypoint.objects.filter(**query)

    def list(self, request):
        data = request.query_params
        query = {'deleted': False, 'active': True}
        groups = request.user.client.groups.filter(active=True)
        if 'postal_code' in data.keys():
            postal_code = get_object_or_404(PostalCode, code=data['postal_code'])
            query['address__in'] = get_postal_code_address_list(postal_code)
        waypoints = get_waypoints_for_groups(groups, query)
        serializer = WaypointListSerializer(waypoints, many=True)
        return Response(serializer.data)


class APIWaypointsLite(ListModelMixin, GenericViewSet):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """
        Return a list of all waypoints from the client.
        """
        query = {'deleted': False, 'active': True}
        groups = request.user.client.groups.filter(active=True)
        waypoints = get_waypoints_for_groups(groups, query)
        serializer = WaypointLiteSerializer(waypoints, many=True)
        return Response(serializer.data)


class APIPostalWaypointIds(RetrieveModelMixin, GenericViewSet):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        """
        Return a list of all waypoints from the client.
        """
        postal_code = pk
        query = {'deleted': False, 'active': True}
        groups = request.user.client.groups.filter(active=True)
        if postal_code:
            postal_code = get_object_or_404(PostalCode, code=postal_code)
            query['address__in'] = get_postal_code_address_list(postal_code)
        waypoints = get_waypoints_for_groups(groups, query)
        serializer = WaypointSerializer(waypoints, many=True)
        return Response(serializer.data)
