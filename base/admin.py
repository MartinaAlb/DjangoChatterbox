from django.contrib import admin
from django.contrib.admin import ModelAdmin

from base.models import Room, Message

class MessageAdmin(ModelAdmin):
    # ListView
    @staticmethod
    def cleanup_body(modeladmin, request, queryset):
        queryset.update(body="--- Deleted ---")

    ordering = ['id']
    list_display = ['id', 'body_short', 'room']
    list_display_links = ['body_short']
    list_per_page = 20
    list_filter = ['room']
    search_fields = ['body', 'id']
    # searche_fields nesmí být cizí klíč, jen ty vlastní klíče - zjistíme v Models
    actions = ['cleanup_body']

    # FormView
    fieldsets = [
        (None, {'fields': ['id', 'body']}),
        ('Detail', {'fields': ['created', 'updated'],
                    'description': ['Detailed information about room']}),
        ('User information', {'fields': ['user']}),
    ]
    readonly_fields = ['id', 'created', 'updated']


# Register your models here.
admin.site.register(Room)
admin.site.register(Message, MessageAdmin)
