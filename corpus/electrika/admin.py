from django.contrib import admin

# Register your models here.
from .models import ElectrikaUser, Team, Announcement, Invite

admin.site.register(ElectrikaUser)
admin.site.register(Team)
admin.site.register(Announcement)
admin.site.register(Invite)