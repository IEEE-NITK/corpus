from django.contrib import admin
from smp.models import Program
from smp.models import ProgramMember
from smp.models import Submission
from smp.models import Upload

# Register your models here.
admin.site.register(Program)
admin.site.register(ProgramMember)
admin.site.register(Upload)
admin.site.register(Submission)
