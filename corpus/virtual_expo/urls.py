from django.urls import include
from django.urls import path
from virtual_expo import views

urlpatterns = [
    path("", views.home, name="virtual_expo_home"),
    path("<int:year>/", views.reports_by_year, name="virtual_expo_reports_by_year"),
    path("report/<int:report_id>", views.report, name="virtual_expo_report"),
    path("members/", include("virtual_expo.member_urls")),
]
