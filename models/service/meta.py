#!/usr/bin/python
#coding=utf8

import yaml
import os,sys,time
from django.conf import settings
from base import Base

class ServiceMeta(object):
	
	@staticmethod
	def get_meta_list(request):
		'''
			读取filelist文件目录
		'''
		filename = settings.DIR[request.GET.get('dir_key')] 
		game = os.popen('cat %s' % settings.DIR['game']).read()
		filepath = filename.format(game = game.rstrip('\n'))
		filelist = Base.get_file_list(filepath,'yaml')
		return filelist
	
	@staticmethod
	def get_meta_content(request):
		'''
			读取meta文件内容
		'''
		filename = request.GET.get('filename')
		content = Base.get_file_content(filename)
		return content
			
	@staticmethod
	def save_yaml_content(request):
		'''
			写入yaml
		'''
		filename = request.POST.get('filename')
		content = request.POST.get('content')
 		Base.save_yaml_content(filename,yaml.load(content))
    	
	