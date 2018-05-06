# from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .models import PostalCode


# Create your views here.
def get_postal_codes(request, id_state):
    postal_codes = serializers.serialize('json',
                                         PostalCode.objects.filter(state=id_state),
                                         fields=('id', 'code'))
    return JsonResponse({'postal_codes': postal_codes})
