"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
import os
from django.contrib import admin
from django.urls import path, include

from django.views.generic import RedirectView

admin.site.site_url = os.environ.get('FRONTEND_URL', 'http://localhost:5173')

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
