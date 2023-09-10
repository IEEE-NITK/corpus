from django.contrib import admin

from .models import Society


# Define the fields to be displayed in the admin panel
class SocietyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


admin.site.register(Society, SocietyAdmin)
