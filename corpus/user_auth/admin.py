from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user_auth.models import CorpusUser

# Register your models here.
admin.site.register(CorpusUser, UserAdmin)
