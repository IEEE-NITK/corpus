from django.contrib import admin
from impulse.models import Announcement
from impulse.models import ImpulseUser
from impulse.models import Team
from impulse.models import Invite
# Register your models here.

admin.site.register(ImpulseUser)
admin.site.register(Team)
admin.site.register(Announcement)
admin.site.register(Invite)