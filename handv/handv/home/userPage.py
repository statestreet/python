#coding=utf-8
from django.template import Context,loader
from django.http import HttpResponse
from handv.home.models import * 
import logging
import md5
from handv.home.page import *
logger = logging.getLogger(__name__)

def interceptor(func):
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

def doLogin(request):  
    username = request.POST['username']
    password = request.POST['password']
    if username=='' or password=='':
        return result("请输入用户名或者密码！")
    m = User.objects.filter(username=username)      
    pwd = md5.new(request.POST['password'])
    pwd.digest()
    if len(m)!=0:
        if  m[0].password == pwd.hexdigest():
            if m[0].state=='0':
                return result("帐号没有激活。请先登录邮箱或者联系一休激活帐号。")
            else:
                request.session['user'] = m[0]
                return home(request)
        else:
            return result("用户名或者密码错拉！")
    else:
        return result("用户名或者密码错拉！")
    
@interceptor
def home(request):  
    user = request.session['user']
    c = Context({'user':user}) 
    t = loader.get_template('home.html')
    return HttpResponse(t.render(c))