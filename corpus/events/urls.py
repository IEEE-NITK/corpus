from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.dashboard, name="events_dashboard"),
    path("core_dashboard", views.core_dashboard, name="events_core_dashboard"),
    path("new", views.new, name="new"),
    path("manage_event/<int:pk>", views.manage_event, name="manage_event"),
    path("delete_event/<int:pk>", views.delete_event, name="delete_event"),
    path("show_event/<int:pk>", views.show_event, name="show_event"),
    path("report/<int:pk>", views.report, name="report"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
