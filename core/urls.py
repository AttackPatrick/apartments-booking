"""
URL configuration for core project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from site_config.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('apartments.url')),
    path('', include('static_pages.url')),
    path('terms-of-use/', terms_of_use_view, name='terms_of_use'),
    path('privacy-policy/', privacy_policy_view, name='privacy_policy'),
    path('environmental-policy/', environmental_policy_view, name='environmental_policy'),
]
urlpatterns += [path(r'^i18n/', include('django.conf.urls.i18n')),]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
