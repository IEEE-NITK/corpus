from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import ModuleConfiguration
from .models import SIG
from .models import Society


class SocietyAdmin(admin.ModelAdmin):
    list_display = ("name", "has_image", "has_dark_image", "linked_sigs", "faculty_advisors", "url")
    list_display_links = ("name",)
    search_fields = ("name", "description", "url")
    list_filter = ("sigs",)
    filter_horizontal = ("sigs",)
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "url", "description"),
            "description": "Core society information"
        }),
        ("Images", {
            "fields": ("image", "dark_image"),
            "description": "Upload society logos (light and dark mode versions)"
        }),
        ("SIG Association", {
            "fields": ("sigs",),
            "description": "Link this society to relevant SIGs"
        }),
    )
    
    def has_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 4px; object-fit: contain;" />',
                obj.image.url
            )
        return format_html('<span style="color: #dc3545;">No image</span>')
    has_image.short_description = "Light Image"
    
    def has_dark_image(self, obj):
        if obj.dark_image:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 4px; object-fit: contain; background: #333;" />',
                obj.dark_image.url
            )
        return format_html('<span style="color: #999;">No dark image</span>')
    has_dark_image.short_description = "Dark Image"
    
    def linked_sigs(self, obj):
        sigs = obj.sigs.all()
        if sigs:
            badges = []
            for sig in sigs:
                color = sig.color if sig.color else "#6b7280"
                badges.append(
                    f'<span style="background-color: {color}; color: white; '
                    f'padding: 2px 6px; border-radius: 3px; margin-right: 3px; '
                    f'font-size: 10px; display: inline-block;">{sig.name}</span>'
                )
            return format_html("".join(badges))
        return format_html('<span style="color: #6c757d;">No SIGs</span>')
    linked_sigs.short_description = "Linked SIGs"
    
    def faculty_advisors(self, obj):
        from accounts.models import Faculty
        count = Faculty.objects.filter(society=obj).count()
        if count > 0:
            return format_html(
                '<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 3px;">{} advisor{}</span>',
                count,
                's' if count != 1 else ''
            )
        return format_html('<span style="color: #6c757d;">No advisors</span>')
    faculty_advisors.short_description = "Faculty Advisors"


class SIGAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "has_image", "event_count", "society_count", "view_events_link")
    list_display_links = ("name",)
    search_fields = ("name", "slug", "about", "what_we_do")
    list_filter = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "color"),
            "description": "Core SIG identification and branding"
        }),
        ("Visual Content", {
            "fields": ("sig_image",),
            "description": "Upload or update the SIG's featured image"
        }),
        ("About Section", {
            "fields": ("about",),
            "description": "Edit the 'About Us' section displayed on the SIG page",
            "classes": ("wide",)
        }),
        ("What We Do Section", {
            "fields": ("what_we_do",),
            "description": "Edit the 'What We Do' section describing SIG activities",
            "classes": ("wide",)
        }),
    )
    
    def has_image(self, obj):
        if obj.sig_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 4px;" />',
                obj.sig_image.url
            )
        return format_html('<span style="color: #dc3545;">No image</span>')
    has_image.short_description = "SIG Image"
    
    def event_count(self, obj):
        count = obj.events.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">{} events</span>',
                count
            )
        return format_html('<span style="color: #6c757d;">No events</span>')
    event_count.short_description = "Events"
    
    def society_count(self, obj):
        count = obj.societies.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #6610f2; color: white; padding: 3px 8px; border-radius: 3px;">{} societ{}</span>',
                count,
                'ies' if count != 1 else 'y'
            )
        return format_html('<span style="color: #6c757d;">No societies</span>')
    society_count.short_description = "Societies"
    
    def view_events_link(self, obj):
        url = reverse("newsletter_manage_announcements")
        return format_html(
            '<a href="{}" class="button" style="background-color: #007bff; color: white; '
            'padding: 5px 12px; border-radius: 4px; text-decoration: none; display: inline-block;">'
            'Manage Events</a>',
            url
        )
    view_events_link.short_description = "Events Dashboard"
    
    def get_readonly_fields(self, request, obj=None):
        if obj: 
            return self.readonly_fields
        return self.readonly_fields
    
    class Media:
        css = {
            'all': ('admin/css/widgets.css',)
        }


admin.site.register(Society, SocietyAdmin)
admin.site.register(ModuleConfiguration)
admin.site.register(SIG, SIGAdmin)
