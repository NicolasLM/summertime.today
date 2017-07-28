from django.contrib import admin

from . import models


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    readonly_fields = ('has_dst', 'offset_to_utc')


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
