#!/usr/bin/python
#coding=utf8

import os
import yaml
from django.conf import settings
import time
import sh,sys
import subprocess

class Base(object):
    
    @staticmethod
    def get_file_list(filepath,flagstr='',flag=1):
        '''
            获取要展示的文件列表
        '''
        filelist = []
        fullfilelist = []
        filenames = os.listdir(filepath)
        if len(filenames) > 0:
            for fn in filenames:
                if len(flagstr)>0:
                    if flagstr in fn:
                        fullfilename = os.path.join(filepath,fn)
                        fullfilelist.append(fullfilename)
                        filelist.append(fn)
                else:
                    fullfilename = os.path.join(filepath,fn)
                    fullfilelist.append(fullfilename)
                    filelist.append(fn)
        if len(filelist) > 0:
            filelist.sort()
            fullfilelist.sort()
            
        return filelist if flag == 0 else fullfilelist
    
    
    @staticmethod
    def get_file_content(filename):
        '''
            获取文件内容
        '''
        all_the_text = ''
        file_object = open(filename)
        try:
            all_the_text = file_object.read()
        finally:
            file_object.close()
        
        return all_the_text
    
    @staticmethod
    def get_yaml_content(filename):
        '''
            获取yaml文件内容
        '''
        f = open(filename)
        data = yaml.load(f)
        f.close()
        return data
    
    @staticmethod
    def save_yaml_content(filename,content):
        '''
            写入yaml
        '''

        game = os.popen('cat %s' % settings.DIR['game']).read()
        bakdir = "%s/bak" % (settings.DIR['meta'].format(game = game.rstrip('\n')))
        bak_filename = "%s/%s_%s" % (bakdir,time.strftime("%Y%m%d%H%M%S", time.localtime()),filename.split("/")[-1])
        if not os.path.isdir(bakdir):
            os.system("mkdir %s" % bakdir)
        os.system("cp %s %s" % (filename,bak_filename))
        
        file_object = open(filename,'w')
        try:
            yaml.dump(content,default_flow_style=False,stream=file_object,indent=4)
        except Exception,e:
            current_content = Base.get_yaml_content(bak_filename)
            yaml.dump(current_content,default_flow_style=False,stream=file_object,indent=4)
            raise e
        file_object.close()
        try:
            os.chdir(os.path.join(settings.DIR['game_admin_script'],'daily'))#切换目录
            repush_meta_cmd = sh.bash.bake('repush_meta.sh')
            repush_meta_cmd(_out=sys.stdout, _err=sys.stderr)
        except Exception,e:
            raise e
    
    @staticmethod
    def remove_grayscale(section):
        '''
            删除区服灰度
        '''
        
        if not section : return False
        
        os.chdir(settings.DIR['game_admin_script'])#切换目录
        try:
            python_script = "remove_grayscale.py"
            args = [settings.DIR['python_path'],python_script]
            
            args.append("-s")
            args.append(section)
            
            subprocess.Popen(args)

        except Exception,e:
            raise e 
        
 
        