from django.contrib import admin
from exchange import models as exchange_models


@admin.register(exchange_models.Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['date', 'currency_from', 'currency_to', 'rate', 'average_last_week']

    def save_model(self, request, obj, form, change):
        exchange_models.Exchange.save_swap(obj)
        super(ExchangeAdmin, self).save_model(request, obj, form, change)

    def average_last_week(self, obj):
        return obj.average_week(obj.date, obj.currency_from, obj.currency_to)['rate__avg']
    average_last_week.short_description = 'Rate average for last week'


@admin.register(exchange_models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name']
