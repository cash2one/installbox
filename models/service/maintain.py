#!/usr/bin/python
#coding=utf8

import yaml
import os,sys,time
from django.conf import settings
from base import Base
import sh
import subprocess

class ServiceMaintain(object):
	
	@staticmethod
	def exec_maintain(request):
		'''
			区服维护
		'''
		kick_user = int(request.GET.get('kick_user',0))
		type = request.GET.get('type','all')
		
		result = []
		try:
			os.chdir(settings.DIR['game_admin_script'])#切换目录
			python_script = "maintain.py"
			args = [settings.DIR['python_path'],python_script]
			
			if type == 'all':
				result.append('all')
			else:
				section = request.GET.get('hdf_info','')
				section_list = section.split(',')
				
				for info in section_list:
					args.append('-s')
					args.append(info)
					result.append(info)
				
				if kick_user == 1:
					args.append('kick_user')
					args.append('1')
				
			subprocess.Popen(args)
			time.sleep(1)
		except Exception,e:
			raise e
		
		return result
		
	@staticmethod
	def remove_maintain(request):
		
		section = request.GET.get('section','')
		if not section: return False
		
		os.chdir(settings.DIR['game_admin_script'])#切换目录
		
		try:
			python_script = "maintain.py"
			args = [settings.DIR['python_path'],python_script]
			args.append('-p')
			args.append('remove')
			if section != 'all':
				args.append('-s')
				args.append(section)
				
			subprocess.Popen(args)
			time.sleep(1)
			return []
		except Exception,e:
			print e
		
		
		
	@staticmethod
	def get_maintain_list():
		'''
			获取区服维护列表
		'''
		
		gamename = sh.cat(settings.DIR['game']).strip("\n")
		filepath = settings.DIR['meta'].format(game=gamename)
		meta_filename = '{filepath}/meta.yaml'.format(filepath=filepath)
		section_filename = '{filepath}/section.yaml'.format(filepath=filepath)
		
		meta_content = Base.get_yaml_content(meta_filename)
		
		data = []
		if 'maintain' in meta_content: #整体维护
			temp={'section':'all'}
			data.append(temp)
			
		else: #区服维护
			
			section_content = Base.get_yaml_content(section_filename)
			
			if 'sections' in section_content:
				for i in section_content['sections']:
					temp = {}
					if 'maintain' in i and i['maintain'] == 1:
						temp['section'] = i['id']
						data.append(temp)
		
		return data
				
						
			
		

	
    	
	