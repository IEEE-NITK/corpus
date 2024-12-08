from django.contrib import admin

from .models import Post
from .models import Tag

admin.site.register(Post)
admin.site.register(Tag)
