from django.contrib import admin
from .models import Waypoint, WaypointGroup, Entity

admin.site.register(Waypoint)
admin.site.register(WaypointGroup)
admin.site.register(Entity)
