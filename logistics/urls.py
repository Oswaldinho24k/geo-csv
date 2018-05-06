from django.conf.urls import url
from .views import get_postal_codes

app_name = 'logistics'

urlpatterns = [
    url(r'^postal_codes/(?P<id_state>[0-9]+)$', get_postal_codes, name='state_postal_codes'),
]
