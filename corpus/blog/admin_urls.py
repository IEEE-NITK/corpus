from blog import admin_views as views
from django.urls import path

urlpatterns = [
    path("dashboard/", views.dashboard, name="blog_admin_dashboard"),
    path("<int:blog_id>/manage/", views.manage, name="blog_admin_manage"),
]
