#!/usr/bin/python
#coding=utf8

import yaml
import os,sys,time
from django.conf import settings
from base import Base

class ServiceHistory(object):
	
	@staticmethod
	def get_log_list():
		'''
			读取filelist文件目录
		'''
		path = settings.DIR['game_admin_script'] 
		filepath = "%s/log/" % path
		filelist = Base.get_file_list(filepath,'all',0)
		filelist.sort(reverse=True)
		return filelist
	
	@staticmethod
	def get_log_content(request):
		'''
			读取meta文件内容
		'''
		filename = "{path}/log/{name}.log".format(path=settings.DIR['game_admin_script'],name=request.GET.get('filename'))
		content = Base.get_file_content(filename)
		return content
			
	
    	
	