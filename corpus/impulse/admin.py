from django.contrib import admin
from impulse.models import Announcement
from impulse.models import ImpulseUser
from impulse.models import Team
# Register your models here.

admin.site.register(ImpulseUser)
admin.site.register(Team)
admin.site.register(Announcement)