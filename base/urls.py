from django.conf.urls import url
from .views import home, base_files
from rest_framework_swagger.views import get_swagger_view

app_name = 'base'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$', base_files, name='base_files'),
    url(r'^docs$', get_swagger_view(title='iuPick API'), name='api_docs'),
]
