from django.urls import include
from django.urls import path

# DO NOT EDIT!
# This file is used for convenience since nginx routes all requests
# to the /api/ endpoint.
urlpatterns = [path("api/", include("corpus.urls"))]
