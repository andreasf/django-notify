from django.contrib import admin
from models import Destination, Challenge


class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    fields = ('name', 'email', 'key')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name',  'key']
        else:
            return []


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('destination', 'valid_until')
    fields = ('destination', 'valid_until', 'code')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['destination', 'valid_until', 'code']
        else:
            return ['valid_until', 'code']


admin.site.register(Destination, DestinationAdmin)
admin.site.register(Challenge, ChallengeAdmin)
