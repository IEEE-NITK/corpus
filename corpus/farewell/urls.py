from django.contrib import admin
from django.urls import include
from django.urls import path

from .views import index

urlpatterns = [
    path("<str:pk>", index, name='farewell'),
    path("", index, name='farewell'),
]
