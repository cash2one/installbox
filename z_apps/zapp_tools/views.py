#!/usr/bin/python
#coding=utf-8

# Create your views here.

import md5
import json
import requests
import time,datetime


__all__ = ["Api"]
class Api(object):
    '''获取基础信息中信息'''

    def __init__(self):
        super(Api, self).__init__()

        self._key = "zhengyingying_cangjinggeadmin"
        self._secret = "974d2147e827caca696b23ddcb5b4b0e"
        self._url = "http://api.web.playcrab.com/service.json"


    def get_data(self,**params):
        data = params.get('json_str','')
        headers = {}
        url = self._url
        headers['content-type'] = 'application/json-rpc'
        headers['type'] = 'application/json-rpc'
        headers['Date'] = self.atom_time()
        print("data=%s"%data)
        json_dict = json.loads(data,strict=False)
        token = self.get_token(params=json_dict['params'],now=headers['Date'])
        headers['Authorization'] = 'PLAYCRAB %s:%s'%(self._key,token)
        try:
            r = requests.post(url, data=data, headers=headers,timeout=3)
            return json.loads(r.text)
        except Exception,e:
            print e.message


    def get_token(self, **params):
        param_data = params.get('params', {})
        uid = params.get('uid','')
        secret = self._secret
        now = params.get('now', '')
        params_sorted = sorted(param_data.iteritems(),key=lambda a:a[0])
        params_str = self.convert_dict_to_str(params=params_sorted)
        s = params_str + secret + now
        md5_str = md5.new(s.encode("utf-8"))
        return md5_str.hexdigest()


    def atom_time(self):
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%dT%H:%M:%S+08:00')


    def convert_dict_to_str(self, **params):
        glue = params.get('glue', '')
        param_data = params.get('params',[])
        str_data = ''
        if param_data:
            for k , v in param_data:
                tmp_str = ''
                if type(v) == tuple or type(v) == list:
                    v = sorted(v)
                    tmp_str = glue.join(v)
                    str_data += k + tmp_str + glue
                else:
                    str_data += k + v + glue
        return str_data
