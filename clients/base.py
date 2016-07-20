#!/usr/bin/python
#coding=utf8

import requests
import random
from .config import settings
import time
import hashlib
import json

__ALL__=['Base']

class Base():
    
    def __init__(self):        
        self.header_authorization_prefix = "PLAYCRAB"
    
    def post(self,current_method,data,url_path):
        '''
            send
        '''
        params = self.requestParam(data,current_method)
        headers = self.requestHeader(params)
        r = requests.post(self.getApiUrl(url_path),data=json.dumps(params),headers=headers)
        return json.loads(r.text)
    
    def requestHeader(self,data):
        '''
            header
        '''
        ISOTIMEFORMAT='%Y-%m-%dT%X+08:00'
        date = time.strftime(ISOTIMEFORMAT,time.localtime())
        token_str = '%s%s%s' % (self.convertDictToStr({'params':data,'glue':""}),settings['api_secret_key'],date)
        token = hashlib.md5(token_str.encode(encoding="utf-8"))
        authorization = "%s %s:%s" % (self.header_authorization_prefix,settings['api_key'],token.hexdigest())
        header = {'Content-Type' : 'application/json','Date' : date,'Authorization' : authorization}
        return header
    
    def requestParam(self,data,current_method):
        '''
            整理参数
        '''
        params = {
            'id' : '1',
            'method' : current_method,
            'params' : data,
            'jsonrpc' : '2.0'
        }
        
        return params;
    
    def getApiUrl(self,url_path):
        '''
            获取URL
        '''
        return "%s%s" % (settings['api_url'],url_path)
    
    def convertDictToStr(self,params):
        '''
            字典转化成字符串
        '''
        glue = params.get('glue', '')
        param_data = params.get('params', '')
        str_data = ''
        if param_data:
            for k , v in param_data.items():
                tmp_str = ''
                if type(v) == tuple or type(v) == list or type(v) == dict:
                    v = sorted(v)
                    tmp_str = glue.join(v)
                    str_data += k + tmp_str + glue
                else:
                    str_data += k + v + glue
        return str_data