#!/usr/bin/python
#coding=utf8

from .base import Base

__ALL__=['Common']
class Common(Base):
    
    def loginUrl(self,callback_url):
        '''获取登陆地址'''
        params = {}
        params['callback'] = callback_url
        return self.post('loginUrl',params,'common/rpc')
    
    def logoutUrl(self,callback_url):
        params = {}
        params['callback'] = callback_url
        return self.post('logoutUrl',params,'common/rpc')
    
    def checkToken(self,token):
        '''验证token'''
        params = {}
        params['token'] = token
        return self.post('checkToken',params,'common/rpc')
    
    
    