"""redoflair URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path, include
from flair.views import FlairLogoutView, FlairLoginView


urlpatterns = [
    path('', include('flair.urls')),
    # path('flair/', include('flair.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', view=FlairLoginView.as_view(), name='login'),
    path('accounts/logout/', view=FlairLogoutView.as_view(), name='logout'),
    path('accounts/', include('allauth.urls')),
]
