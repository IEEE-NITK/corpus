from django.urls import path
from virtual_expo import admin_views as views

urlpatterns = [
    path("dashboard/", views.dashboard, name="virtual_expo_admin_dashboard"),
    path("<int:report_id>/manage/", views.manage, name="virtual_expo_admin_manage"),
]
