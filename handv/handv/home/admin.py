'''
Created on 2012-4-3

@author: yixiugg
'''
from django.template import Context,loader
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def adminInterceptor(func):
    logger.info('interceptor function : %s ' % func.__name__);
    def wapper(request,*args,**kargs):
        if 'user' in request.session and request.session['user']:
            try:
                response =  func(request,*args,**kargs)
                return response
            except Exception,e:
                print e
                return HttpResponse("error")
        else:
            return login(request)
    return wapper

def login(request):  
    c = Context({'result':'You must login!'}) 
    t = loader.get_template('login.html')
    return HttpResponse(t.render(c))