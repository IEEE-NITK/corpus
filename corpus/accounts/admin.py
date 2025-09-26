from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Core
from .models import ExecutiveMember
from .models import Faculty
from .models import Post
from .models import User

# Register your models here.


class CorpusUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "phone_no", "gender", "profile_pic")},
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
    list_display = ("email", "first_name", "last_name", "phone_no", "gender", "profile_pic")
    search_fields = ("email", "first_name", "last_name", "phone_no")
    ordering = ("email",)


class ExecutiveMemberAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("user", "sig")}),
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
            {"fields": ("ieee_number", "ieee_email", "profile_picture")},
        ),
        ("Socials", {"fields": ("linkedin", "hide_linkedin", "github", "hide_github")}),
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


class CoreAdmin(admin.ModelAdmin):
    list_display = ("executivemember", "society", "post", "term_start")


class FacultyAdmin(admin.ModelAdmin):
    list_display = ("user", "sig", "post", "term_start")


class PostAdmin(admin.ModelAdmin):
    list_display = ("name", "priority")


admin.site.register(User, CorpusUserAdmin)
admin.site.register(ExecutiveMember, ExecutiveMemberAdmin)
admin.site.register(Core, CoreAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Post, PostAdmin)
