#!/usr/bin/python
#coding=utf8

import yaml
import os,sys,time
from django.conf import settings
from base import Base
import sh

class ServiceGrayscale(object):
	
	@staticmethod
	def get_grayscale_section():
		'''
			读取meta文件内容
		'''
		gamename = sh.cat(settings.DIR['game']).strip("\n")
		filepath = settings.DIR['meta'].format(game=gamename)
		filename = "{path}/version.yaml".format(path=filepath)
		content = Base.get_yaml_content(filename)
		
		result = []
		if 'version' in content:
			for k,v in content['version'].items():
				if k == 'all': continue
				temp = {}
				temp['section'] = k
				temp['upgrade'] = v[0]['upgrade_path']
				temp['version'] = v[0]['version']
				result.append(temp)
			
		return result
	
	
	@staticmethod
	def remove_grayscale(request):
		'''
			删除区服灰度
		'''
		section = request.GET.get('section')
		
		if not section:return
		
		Base.remove_grayscale(section)
			
	
    	
	