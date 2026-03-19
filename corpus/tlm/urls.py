from django.urls import path
from tlm import views

urlpatterns = [
    path('',views.landing,name="tlm_landing")
]