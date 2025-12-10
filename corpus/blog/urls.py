from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<slug:slug>", views.full_post, name="full_post"),
    path("tags/<int:specific_tag>/", views.post_list, name="tagged_blog"),
    # path("tags/<slug:slug>", views.tagged_blog, name="tagged_blog"),
    path("members/", include("blog.member_urls")),
    path("admin/", include("blog.admin_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
