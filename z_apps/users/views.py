#!/usr/bin/python
#coding=utf-8
'''
auth:wuqichao
createtime:2016-2-11 
功能：用户类功能模块
'''
from django.conf import settings
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, ListView, RedirectView

from clients.common import Common
from clients.users import Users
from django.shortcuts import redirect  
import pymysql as MySQLdb


'''
home主页
'''
class HomeView(TemplateView):
    template_name = "users/home.html"


'''
home登录页
'''
class LoginView(RedirectView):
    
    def get(self,request):
        host = request.get_host()
        callback_url = "http://%s/users/check/" % host
        co = Common()
        url = co.loginUrl(callback_url)
        return redirect(url['result'])
        # return render(request,'z_app/ip_list.html')
'''
home登出页
'''
class LogoutView(RedirectView):
    
    def get(self,request):
        response = HttpResponse()
        response.delete_cookie(settings.SESSION_COOKIE_NAME)
        if "username" in request.session:
            del request.session["username"]

        host = request.get_host()
        callback_url = "http://%s/userslogin/" % host
        co = Common()
        url = co.logoutUrl(callback_url)
        return redirect(url['result'])

class ErrorView(TemplateView):
    
    template_name = "users/error.html"

'''
账号密码验证
'''
class CheckView(RedirectView):
    
    permanent = False
    query_string = True
    
    def get(self, request):
        '''get方式'''
        token = request.GET.get("token")
        co = Common()
        data = co.checkToken(token)
        
        self.pattern_name = "users:error"
        if data['result']:
            usersModel = Users()
            user = usersModel.getUserById(data['result'])
            user_role = usersModel.getRolesById(data['result'])
            if user_role['result']:
                response = HttpResponse()
                response.set_cookie(settings.SESSION_COOKIE_NAME,user['result']['name'] )
                request.session["username"] = user['result']['name']
                self.pattern_name = "users:home"

        return redirect(reverse(self.pattern_name, args=[]))  
#         return super(CheckView, self).get(request)
    
#     #post方式接收验证
#     def post(self, request, *args, **kwargs):
#  
#         post_data = request.POST
#  
#         #做一个假的账号密码验证
#         if post_data['username'] == "admin@playcrab.com" and post_data['passwd'] == "123456":
#  
#             response = HttpResponse(self.url)
#             response.set_cookie(settings.SESSION_COOKIE_NAME,post_data['username'] )
#             request.session["username"] = post_data['username'] 
#  
#         
#             self.pattern_name = "users:home"
#             
#         else:
#  
#             self.pattern_name = "users:login"
#          
#         return super(CheckView, self).post(request, *args, **kwargs)

