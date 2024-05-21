from django.contrib import admin

from .models import ModuleConfiguration
from .models import SIG
from .models import Society


# Define the fields to be displayed in the admin panel
class SocietyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class SIGAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)


admin.site.register(Society, SocietyAdmin)
admin.site.register(ModuleConfiguration)
admin.site.register(SIG, SIGAdmin)
