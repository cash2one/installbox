#!/usr/bin/python
#coding=utf8

import yaml
import os,sys,time
from django.conf import settings
from base import Base
import sh
import commands
import subprocess
import requests

class ServiceVersion(object):

    @staticmethod
    def get_all_upgrade(request):
        '''
        	获取所有升级序列
        '''
        filepath = settings.DIR[request.GET.get("dir_key")]
        list = Base.get_file_list(filepath, 'yaml')
        data = []
        for info in list:
            temp_data = Base.get_yaml_content(info)
            data.append(temp_data['upgrade_path'])
         
        return set(data)
	 
    @staticmethod
    def get_all_release(request):
        '''
            根据升级序列获取版本
        '''
        filepath = settings.DIR[request.GET.get("dir_key")]
        upgrade_path = request.GET.get('upgrade')
        list = Base.get_file_list(filepath, 'yaml',1)
        data = []
        for info in list:
            temp_data = Base.get_yaml_content(info)
            if upgrade_path == temp_data['upgrade_path']:
                data.append(temp_data['version'])
        
        data.sort(reverse=True)
        return data
    
    @staticmethod
    def fat_version(request):
        release_list = request.GET.getlist("release")
        if not release_list: 
            return False
        
        hdf_info = request.GET.get('hdf_info','') #灰度服信息
        remove_hdf = request.GET.get('remove_hdf','') #要删除的灰度服信息
        remove = int(request.GET.get('remove',0))
        
        if remove == 1:
			#删除灰度服
			try:
				for section in remove_hdf.split(","):
					Base.remove_grayscale(section)
			except Exception,e:
				raise e
		
        try:
            
            os.chdir(os.path.join(settings.DIR['game_admin_script'],'daily'))
            
            python_script = "change_version.py"
            
            args = [settings.DIR['python_path'],python_script]
			
            if int(request.GET.get('update_tools',0)) == 1:
			 	args.append('-u')
			 	args.append('1')
			 	
            for release in release_list:
				args.append('-v')
				args.append(release)
            
            if hdf_info:
 				for section in hdf_info.split(','):
				 	args.append('-s')
					args.append(section)
			
            subprocess.Popen(args)

            return []
        except Exception,e:
			raise e
			
			
    @staticmethod
    def get_log(request):
        log_path = '%s/log/operate_log.log' % settings.DIR['game_admin_script']
        if os.path.exists(log_path):
            output = os.popen('cat {log_path}'.format(log_path=log_path))
            return output.read()
        else:
            raise Exception('log error')