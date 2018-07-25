from datetime import date, timedelta

from django.db import models
from django.db.models import Avg, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver


class Currency(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Exchange(models.Model):
    date = models.DateField()
    currency_from = models.ForeignKey(Currency)
    currency_to = models.ForeignKey(Currency, related_name='currency_to')
    rate = models.DecimalField(decimal_places=8, max_digits=14)

    class Meta:
        unique_together = ('date', 'currency_from', 'currency_to')

    def __str__(self):
        return str(self.date)

    @staticmethod
    def average_week(obj_date, currency_from, currency_to):
        d= obj_date - timedelta(days=7)
        average = Exchange.objects.filter(currency_from=currency_from, 
                                        currency_to=currency_to, 
                                        date__range=(d, obj_date)
                                        ).aggregate(Avg('rate'))
        return average

    @staticmethod
    def save_swap(obj):
        try:
            if obj.currency_from == obj.currency_to:
                Exchange.objects.create(date= obj.date, 
                                        currency_from = obj.currency_to,
                                        currency_to = obj.currency_from, 
                                        rate = obj.rate)   
            else:
                Exchange.objects.create(date= obj.date,
                                        currency_from = obj.currency_to,
                                        currency_to = obj.currency_from,
                                        rate = 1/obj.rate)   
        
        except Exception:
            pass
