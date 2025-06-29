from blog import member_views as views
from django.urls import path

urlpatterns = [
    path("dashboard/", views.dashboard, name="blog_dashboard"),
    path("blog/new/", views.new_blog, name="blog_new_blog"),
    path(
        "blog/<slug:slug>/edit/",
        views.edit_blog,
        name="blog_edit_blog",
    ),
    path(
        "preview/<slug:slug>/",
        views.preview_blog,
        name="blog_preview_blog",
    ),
    path(
        "approver_dashboard/",
        views.approver_dashboard,
        name="blog_approver_dashboard",
    ),
]
