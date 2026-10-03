from django.contrib import admin

from .models import Event

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "status", "status_override")
    list_filter = ("status_override",)
