from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf.global_settings import LANGUAGES
from pycountry import currencies as CURRENCIES
from django.contrib.gis.db import models as geo_models
from django.contrib.postgres.indexes import GistIndex


# Create your models here.

class Provider(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100)
    phone_number = PhoneNumberField(blank=False, null=False)
    # probably doesnt have all the languages, but lets say its enough for now
    language = models.CharField(max_length=7, choices=LANGUAGES)
    currency_choices = [(i.alpha_3, i.name) for i in list(CURRENCIES)]
    currency = models.CharField(max_length=3, choices=currency_choices, blank=False, null=False)


class ServiceArea(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    # lest make price an int for the simplicity sake
    price = models.IntegerField(null=False, blank=False)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    polygon = geo_models.PolygonField(spatial_index=True)

    class Meta:
        indexes = [GistIndex(fields=['polygon'])]
