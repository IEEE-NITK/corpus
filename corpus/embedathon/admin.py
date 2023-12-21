from django.contrib import admin
from embedathon.models import Announcement
from embedathon.models import EmbedathonUser
from embedathon.models import Invite
from embedathon.models import Team

# Register your models here.

admin.site.register(EmbedathonUser)
admin.site.register(Team)
admin.site.register(Invite)
admin.site.register(Announcement)
