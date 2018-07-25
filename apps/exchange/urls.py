from django.conf.urls import include, url
from tastypie.api import Api

from exchange import api as exchange_api

v1_api = Api(api_name='v1')
v1_api.register(exchange_api.ListExchangeResources())
v1_api.register(exchange_api.CreateExchangeResources())

urlpatterns = [
    url(r'', include(v1_api.urls)),
]