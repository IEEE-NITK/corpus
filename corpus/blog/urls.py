from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<slug:slug>", views.full_post, name="full_post"),
    path("tags/<int:specific_tag>", views.tagged_blog, name="tagged_blog"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
