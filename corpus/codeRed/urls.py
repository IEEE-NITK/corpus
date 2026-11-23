from codeRed import views
from django.urls import path

urlpatterns = [path("", views.home, name="codeRed_home")]
