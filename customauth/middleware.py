from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import SESSION_KEY
from django.core.urlresolvers import reverse  
from django.contrib import auth
from django.utils.functional import SimpleLazyObject
from django.core.urlresolvers import reverse 
from django.shortcuts import redirect


def get_user(request):

    if not hasattr(request, '_cached_user'):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None) 
        request._cached_user = session_key
    return request._cached_user


class AuthenticationMiddleware(object):

    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        request.user = SimpleLazyObject(lambda: get_user(request))
        
        if request.path_info.startswith('/static/'):
            return None

        
        if request.user == None and request.path_info not in ["/userslogin/","/userscheck/","/userserror/"]:
            return redirect(reverse('users:login', args=[]))  

    



