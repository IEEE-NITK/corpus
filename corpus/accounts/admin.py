from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ExecutiveMember
from .models import User

# Register your models here.


class CorpusUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "phone_no", "gender")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_no",
                    "gender",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "phone_no", "gender")
    search_fields = ("email", "first_name", "last_name", "phone_no")
    ordering = ("email",)


class ExecutiveMemberAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("user", "sig", "date_joined")}),
        (
            "NITK Related Details",
            {
                "fields": (
                    "edu_email",
                    "roll_number",
                    "reg_number",
                    "minor_branch",
                    "is_nep",
                )
            },
        ),
        (
            "IEEE Related Details",
            {"fields": ("ieee_number", "ieee_email")},
        ),
        ("Socials", {"fields": ("linkedin", "github")}),
    )
    list_display = ("user", "sig", "roll_number", "edu_email", "ieee_number", "is_nep")
    search_fields = (
        "roll_number",
        "reg_number",
        "edu_email",
        "ieee_number",
        "ieee_email",
    )
    ordering = ("user",)


admin.site.register(User, CorpusUserAdmin)
admin.site.register(ExecutiveMember, ExecutiveMemberAdmin)
