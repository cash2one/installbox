#!/usr/bin/python
#coding=utf8

from .base import Base

__ALL__=['Users']
class Users(Base):
    
    def getUserById(self,uid = None):
        
        '''获取用户信息'''
        if uid is None: return False
        params = {}
        params['id'] = uid
        return self.post('getUserById',params,'user/rpc')
        
    
    def getRolesById(self,uid = None):
        
        '''获取用户在本项目角色'''
        if uid is None: return False
        params = {}
        params['id'] = uid
        return self.post('getRolesById',params,'user/rpc')
    
    