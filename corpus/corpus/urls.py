"""
URL configuration for corpus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ckeditor_uploader import views as ckeditor_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path
from django.views.decorators.cache import never_cache

urlpatterns = [
    path(
        "ckeditor/upload/",
        login_required(ckeditor_views.upload),
        name="ckeditor_upload",
    ),
    path(
        "ckeditor/browse/",
        never_cache(login_required(ckeditor_views.browse)),
        name="ckeditor_browse",
    ),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("pages.urls")),
    path("embedathon/", include("embedathon.urls")),
    path("impulse/", include("impulse.urls")),
    path("electrika/", include("electrika.urls")),
    path("skyward_expedition/", include("skyward_expedition.urls")),
    path("robotrix/", include("robotrix.urls")),
    path("farewell/", include("farewell.urls")),
    path("virtual_expo/", include("virtual_expo.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
