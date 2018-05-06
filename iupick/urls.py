"""iupick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/

"""
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url('', include('base.urls')),
    url('', include('tosp_auth.urls')),
    url(r'^api/', include('iupick_api.urls')),
    url(r'^administration/', include('administration.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^logistics/', include('logistics.urls')),
    url(r'^user_profiles/', include('user_profiles.urls')),
    url(r'^waypoints/', include('waypoints.urls'))
]
