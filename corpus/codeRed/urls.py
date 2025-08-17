from django.urls import path
from codeRed import views

urlpatterns = [
    path('',views.home,name="codeRed_home")
]