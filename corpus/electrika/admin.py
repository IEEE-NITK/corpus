from django.contrib import admin

from .models import Announcement
from .models import ElectrikaUser
from .models import Invite
from .models import Team

# Register your models here.

admin.site.register(ElectrikaUser)
admin.site.register(Team)
admin.site.register(Announcement)
admin.site.register(Invite)
