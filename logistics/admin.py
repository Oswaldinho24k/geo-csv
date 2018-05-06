from django.contrib import admin
from .models import Address, Carrier, Country, PostalCode, State, Contact, \
                    Shipment, ExternalShipment


class StateAdmin(admin.ModelAdmin):
    fields = ('name', 'code')


admin.site.register(Address)
admin.site.register(Carrier)
admin.site.register(Contact)
admin.site.register(Country)
admin.site.register(ExternalShipment)
admin.site.register(PostalCode)
admin.site.register(Shipment)
admin.site.register(State, StateAdmin)
