from django.urls import path
from virtual_expo import views

urlpatterns = [path("", views.home, name="virtual_expo_home")]
