"""devops URL Configuration


The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL toappurlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns



from z_apps.app import views

urlpatterns = [
                      
    url(r'collection/$', views.CollectionView.as_view(), name="collection"),
    url(r'NodepAdd/$', views.NodepAdd.as_view(), name="NodepAdd"),
    url(r'node/$', views.NodeView.as_view(), name="node"),
    url(r'deploy/$', views.DeployView.as_view(), name="deploy"),
    url(r'filelistjson/$', views.FileListJsonView.as_view(), name="filelistjson"),


    url(r'FailNodeView/$', views.FailNodeView.as_view(), name="FailNodeView"),
    url(r'FileDeployView/$', views.FileDeployView.as_view(), name="FileDeployView"),
    url(r'FillNodeAdd/$', views.FillNodeAdd.as_view(), name="FillNodeAdd"),
    url(r'DeltepNode/$', views.DeltepNode.as_view(), name="DeltepNode"),

    url(r'FileTimeGoView/$', views.FileTimeGoView.as_view(), name="FileTimeGoView"),
    url(r'FileTakeShell/$', views.FileTakeShell.as_view(), name="FileTakeShell"),
    url(r'FillDelteNode/$', views.FillDelteNode.as_view(), name="FillDelteNode")

]