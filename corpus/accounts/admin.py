from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import CorpusChangeForm

# Register your models here.

class CorpusUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_no', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_no', 'gender', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'phone_no', 'gender')
    search_fields = ('email', 'first_name', 'last_name', 'phone_no')
    ordering = ('email',)

admin.site.register(User, CorpusUserAdmin)