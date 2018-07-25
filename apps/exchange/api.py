from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, csrf_exempt, ALL
from tastypie.validation import CleanedDataFormValidation

from exchange import models as exchange_models


class ListExchangeResources(ModelResource):

    class Meta:
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()
        fields = ['date', 'currency_from', 'currency_to', 'rate']
        filtering = {
            'id': ALL,
            'date': ALL
        }
        queryset =  exchange_models.Exchange.objects.all()
        resource_name = 'exchange'

    def dehydrate(self, bundle):
        bundle.data['currency_from'] = bundle.obj.currency_from.name
        bundle.data['currency_to'] = bundle.obj.currency_to.name
        bundle.data['average_rate'] = bundle.obj.average_week(bundle.obj.date, bundle.obj.currency_from, bundle.obj.currency_to)['rate__avg']
        
        return bundle


class CreateExchangeResources(ModelResource):

    class Meta:
        allowed_methods = ['post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        fields = ['date', 'currency_from', 'currency_to', 'rate']
        queryset =  exchange_models.Exchange.objects.all()
        resource_name = 'create-exchange'

    def wrap_view(self, view):
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            request.format = kwargs.pop('format', None)
            wrapped_view = super(CreateExchangeResources, self).wrap_view(view)
            return wrapped_view(request, *args, **kwargs)
        return wrapper

    def hydrate(self, bundle):
        currency_from, created = exchange_models.Currency.objects.get_or_create(name=bundle.data['currency_from'])
        currency_to, created = exchange_models.Currency.objects.get_or_create(name=bundle.data['currency_to'])
        bundle.obj.currency_from = currency_from
        bundle.obj.currency_to = currency_to
        return bundle    

    def obj_create(self, bundle, **kwargs):
        bundle = super(CreateExchangeResources, self).obj_create(bundle, **kwargs)
        exchange_models.Exchange.save_swap(bundle.obj)
        return bundle
