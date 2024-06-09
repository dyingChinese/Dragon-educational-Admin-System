"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.auth.views import LoginView
from django.urls import path, include
from common.views import login
import common.views
from backend import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('courseSystem/', include('courseSystem.urls')),
                  path('infoSystem/', include('infoSystem.urls')),
                  path('statisticsSystem/', include('statisticsSystem.urls')),
                  path('common/', include('common.urls')),
                  path('login', login),
                  # path('login/', common.views.LoginView),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
