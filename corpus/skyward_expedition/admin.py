from django.contrib import admin
from skyward_expedition.models import Announcement
from skyward_expedition.models import Invite
from skyward_expedition.models import SEUser
from skyward_expedition.models import Team


# Register your models here.


class SEUserAdmin(admin.ModelAdmin):
    list_display = ("user", "college_name")
    search_fields = ("user", "college_name")
    ordering = ("user",)


admin.site.register(SEUser, SEUserAdmin)
admin.site.register(Team)
admin.site.register(Invite)
admin.site.register(Announcement)
