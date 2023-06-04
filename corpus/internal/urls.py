from django.urls import path

import internal.views as views

urlpatterns = [
    path("design_system", views.design_system, name="internal_design_system"),
]
