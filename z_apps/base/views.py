#!/usr/bin/python
#coding=utf8

from django.core import serializers
from django import http
import multiprocessing


from django.views.generic import TemplateView, ListView

import os
import json
import base64
import socket
import paramiko
import traceback

from django.conf import settings



def trace_back():
    try:
        return traceback.format_exc()
    except:
        return ''
    

class JSONResponseMixin(object):
    """JSON mixin"""



    def render_to_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        return http.HttpResponse(content,
                            content_type='application/json',
                            **httpresponse_kwargs)

    def convert_context_to_json(self, context):

        #return serializers.serialize("json", context)
        
        return json.dumps(context)




class SSHJsonView(JSONResponseMixin, TemplateView):

    hosts = []
    message = []

    def get(self, request, *args, **kwargs):

        pool = multiprocessing.Pool(processes = 10)
        result = []


        for host in SSHJsonView.hosts:
         
            result.append(pool.apply_async(ssh_cmd, (host,)))

        pool.close()
        pool.join()

        msg = []
        for res in result:
            msg.append(res.get())


        SSHJsonView.message = json.dumps(msg)

       



class ReadDirJsonView(JSONResponseMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):

        from models.service.meta import ServiceMeta
        
        data = ServiceMeta.get_meta_list(request) 

        return self.render_to_response(list(data))
    

class ReadFileJsonView(JSONResponseMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):

        from models.service.meta import ServiceMeta
        
        data = ServiceMeta.get_meta_content(request) 

        return self.render_to_response(data)


class ReadUpgradeJsonView(JSONResponseMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):

        from models.service.version import ServiceVersion
        
        data = ServiceVersion.get_all_upgrade(request) 

        return self.render_to_response(list(data))
    
    
class ReadReleaseJsonView(JSONResponseMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):

        from models.service.version import ServiceVersion
        
        data = ServiceVersion.get_all_release(request) 

        return self.render_to_response(list(data))


