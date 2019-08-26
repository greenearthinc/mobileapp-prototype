"""green_earth_cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from green_earth_app.iot_core import iot_core_router
from green_earth_app.web_app import web_app_router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^iot_core/', iot_core_router, name='iot_core'),
    url(r'^web_app/', web_app_router, name='web_app'),
]
