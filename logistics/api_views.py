import os
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from fedex_wrapper import tracking as fedex_tracking
from estafeta_wrapper import tracking as estafeta_tracking
from tosp_auth.permissions import IsAuthenticatedWithSecret
from .models import Shipment, PostalCode
from .serializers import AddressSerializer, ShipmentSerializer, \
                         InitialShipmentSerializer, FillInformationSerializer, \
                         ExternalShipmentSerializer, PostalCodeSerializer


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def create_address(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'Message': 'Address created successfully'}, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def create_waybill(request):
    """
    Allows you to create an entirely new waybill
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ShipmentSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            waybill = serializer.save()
            if waybill.create_waybill():
                return JsonResponse({'carrier': waybill.carrier.name,
                                     'tracking_number': waybill.tracking_number,
                                     'waybill_link': waybill.waybill_link},
                                    status=201)
            else:
                return JsonResponse({'error': 'Impossible to generate waybill'},
                                    status=500)
        return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes((IsAuthenticatedWithSecret, ))
def create_shipment_token(request):
    """
    Gets the minimum information required for
    creating a new shipment and returns its
    uuid.
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InitialShipmentSerializer(data=data,
                                               context={'request': request})
        if serializer.is_valid():
            shipment = serializer.save()
            return JsonResponse({'shipment_token': shipment.unique_id},
                                status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def fill_shipment_information(request, shipment_token):
    """
    Fills the rest of the missing information for a package
    """
    if request.method == 'POST':
        shipment_data = JSONParser().parse(request)
        
        shipment = Shipment.objects.filter(unique_id=shipment_token).get()
        serializer = FillInformationSerializer(instance=shipment, data=shipment_data)
        
        if serializer.is_valid():
            shipment = serializer.save()
            return JsonResponse({'confirmation_token': shipment.unique_id},
                                status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes((IsAuthenticatedWithSecret, ))
def generate_waybill(request, shipment_token):
    """
    Generates the waybill for a pedido.
    """
    if request.method == 'POST':
        shipment = Shipment.objects.filter(unique_id=shipment_token).get()
        if shipment.waybill_link or shipment.create_waybill():
            return JsonResponse({'carrier': shipment.carrier.name,
                                 'tracking_number': shipment.tracking_number,
                                 'waybill_link': shipment.waybill_link}, status=201)
        return JsonResponse({'error': 'Impossible to generate waybill'}, status=500)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def track_shipment(request):
    if request.method == 'GET':
        data = request.query_params
        carrier = data['carrier']
        tracking_number = data['tracking_number']

        if os.environ['DJANGO_SETTINGS_MODULE'] == 'iupick.settings.production':
            production = True
        else:
            production = False

        if carrier == 'Fedex':
            track_info = fedex_tracking.track(
                production=production,
                key=os.environ['FEDEX_KEY'],
                password=os.environ['FEDEX_PASSWORD'],
                account_number=os.environ['FEDEX_ACCOUNT_NUMBER'],
                meter_number=os.environ['FEDEX_METER_NUMBER'],
                tracking_number=tracking_number
            )

            status_detail = track_info.CompletedTrackDetails[0].TrackDetails[0].StatusDetail
            street_line_dict = dict(enumerate(status_detail.Location.StreetLines))
            response = {'description': status_detail.Description,
                        'address': {'line_one': street_line_dict.get(0, None),
                                    'line_two': street_line_dict.get(1, None),
                                    'city': status_detail.Location.City,
                                    'state_code': status_detail.Location.StateOrProvinceCode,
                                    'postal_code': status_detail.Location.PostalCode,
                                    'country_name': status_detail.Location.CountryName}}
            return JsonResponse(response, status=200)
        if carrier == 'Estafeta':
            track_info = estafeta_tracking.track(
                production=production,
                login=os.environ['ESTAFETA_TRACK_LOGIN'],
                password=os.environ['ESTAFETA_TRACK_PASSWORD'],
                subscriber_id=os.environ['ESTAFETA_TRACK_SUBSCRIBER'],
                waybill=tracking_number
            )

            history_last_event = track_info.trackingData.TrackingData[0].history.History[-1]
            response = {'status': track_info.trackingData.TrackingData[0].statusSPA,
                        'description': history_last_event.eventDescriptionSPA,
                        'dateTime': history_last_event.eventDateTime,
                        'address': history_last_event.eventPlaceName}
            return JsonResponse(response, status=200)
        return JsonResponse({'Message': 'Datos invalidos'}, status=400)


@api_view(['POST'])
@permission_classes((IsAuthenticatedWithSecret, ))
def confirm_waypoint_shipment(request):
    """
    Creates an external shipment associated to the user of the secret token
    and the waypoint they are sending..
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ExternalShipmentSerializer(data=data,
                                                context={'request': request})
        if serializer.is_valid():
            external_shipment = serializer.save()
            return JsonResponse({'shipment_token': external_shipment.unique_id},
                                status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def postal_code_info(request, code):
    if request.method == 'GET':
        print(code)
        postal_code = get_object_or_404(PostalCode, code=code)
        serializer = PostalCodeSerializer(postal_code)
        return Response(serializer.data)
