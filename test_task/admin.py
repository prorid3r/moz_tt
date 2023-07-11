from django.contrib import admin
from .models import Provider


# Register your models here.

class ProviderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Provider, ProviderAdmin)
