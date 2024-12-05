from django.contrib import admin

from .models import Achievement
from .models import Publication
from .models import Tag

admin.site.register(Achievement)
admin.site.register(Publication)
admin.site.register(Tag)
