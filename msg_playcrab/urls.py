"""msg_playcrab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from z_apps.users import views

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    url(r'^users/', include('a_urls.usersurl', namespace='users', app_name='users'), name='users'),
    url(r'^base/', include('a_urls.baseurl', namespace='base', app_name='base'), name='base'),
    url(r'^app/', include('a_urls.appurl', namespace='app', app_name='app'), name='app'),
    url(r'^$', views.LoginView.as_view(), name="index"),
]
