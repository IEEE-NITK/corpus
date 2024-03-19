from django.contrib import admin
from virtual_expo.models import Report
from virtual_expo.models import ReportMember
from virtual_expo.models import ReportType

# Register your models here.
admin.site.register(Report)
admin.site.register(ReportType)
admin.site.register(ReportMember)
