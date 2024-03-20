from django.urls import path
from virtual_expo import views

urlpatterns = [
    path("", views.home, name="virtual_expo_home"),
    path("<int:year>/", views.reports_by_year, name="virtual_expo_reports_by_year"),
]
