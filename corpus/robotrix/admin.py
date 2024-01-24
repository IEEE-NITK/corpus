from django.contrib import admin
from robotrix.models import Announcement
from robotrix.models import Invite
from robotrix.models import RobotrixUser
from robotrix.models import Team

# Register your models here.

admin.site.register(RobotrixUser)
admin.site.register(Team)
admin.site.register(Announcement)
admin.site.register(Invite)
