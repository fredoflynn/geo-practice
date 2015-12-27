from django.contrib import admin

from world.models import Park


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')