from django.urls import path
from virtual_expo import member_views as views

urlpatterns = [
    path("dashboard/", views.dashboard, name="virtual_expo_members_dashboard")
]
