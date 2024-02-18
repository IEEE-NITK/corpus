from django.contrib import admin
from skyward_expedition.models import SEUser


# Register your models here.


class SEUserAdmin(admin.ModelAdmin):
    list_display = ("user", "college_name")
    search_fields = ("user", "college_name")
    ordering = ("user",)


admin.site.register(SEUser, SEUserAdmin)
