"""devops URL Configuration


The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from z_apps.base import views

urlpatterns = [
    
    url(r'readdirjson/$', views.ReadDirJsonView.as_view(), name="readdirjson"),
    url(r'readfilejson/$', views.ReadFileJsonView.as_view(), name="readfilejson"),
    url(r'readupgradejson/$', views.ReadUpgradeJsonView.as_view(), name="readupgradejson"),
    url(r'readreleasejson/$', views.ReadReleaseJsonView.as_view(), name="readreleasejson"),
]