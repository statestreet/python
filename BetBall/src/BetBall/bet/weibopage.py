#coding=utf-8
import datetime,time    
import getpass
import os
import sys
import md5
import json
import random
from weibo import APIClient
from django.template import Context, loader,RequestContext
from django.db.models import Q
from django.http import *
from BetBall.bet.timer import *
from BetBall.bet.models import *  
from BetBall.bet.page import *


#APP_KEY = '3118024522' # app key of betball
#APP_SECRET = '95895b5b4556994a798224902af57d30' # app secret of betball
#CALLBACK_URL = 'http://www.noya35.com/weiboLoginBack' # callback url

APP_KEY = '2945318614' # app key of betball
APP_SECRET = '26540ac5e2728be53005df042bc9bc00' # app secret of betball
CALLBACK_URL = 'http://127.0.0.1:8888/weiboLoginBack' # callback url
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
SITE_URL = 'http://www.noya35.com'

def weiboLogin(request):
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    return HttpResponseRedirect(url) 

def weiboLoginBack(request):
    #得到微博认证的信息
    code = request.GET['code']
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in
    # TODO: 在此可保存access token
    request.session['access_token'] = access_token
    request.session['expires_in'] = expires_in
    client.set_access_token(access_token, expires_in)
    #测试发微博
#    status = u'亲们，俺刚才手快，测试了一把，您别b4啊！'
#    client.post.statuses__update(status=status)
    #得到微博用户的id，如果有绑定，则直接登录，没有则跳到绑定页面
    json_obj = client.get.statuses__user_timeline()
    weibo_user = json_obj['statuses'] [0]['user']
    #得到用户的weibo UID
    weibo = weibo_user['id']
#    request.session['weibo_client'] = client
    request.session['weibo'] = weibo
    #得到用户的微博nick
    weibo_nick = weibo_user['screen_name']
    request.session['weibo_nick'] = weibo_nick
    a = Admin.objects.filter(weibo=weibo)
    #先尝试admin登陆
    if len(a)!=0:
        request.session['admin'] = a[0]
        now = datetime.datetime.now()    
        list = Match.objects.filter(matchtime__gte=now).order_by('-state','matchtime')     
        c = Context({'list':list,'session':request.session}) 
        t = loader.get_template('admin.htm')
        return HttpResponse(t.render(c))
    #尝试用户登陆
    u = Gambler.objects.filter(weibo=weibo)
    if len(u)!=0:
        gambler = u[0]
        request.session['gambler'] = gambler
        gambler.weibo_nick=weibo_nick
        gambler.save()
        return myaccount(request)
    else:
        c = Context({'info':'Please bind your account or register first!','session':request.session}) 
        t = loader.get_template('bind.htm')
        return HttpResponse(t.render(c))
    return HttpResponseRedirect("/") 

def bind(request): 
    m = Gambler.objects.filter(username=request.POST['username'])      
    pwd = md5.new(request.POST['password'])
    pwd.digest()
    if len(m)!=0:
        if  m[0].password == pwd.hexdigest():
            if m[0].state=='0':
                return result("Account not active, please contact admin.")
            else:
                gambler = m[0]
                request.session['gambler'] = gambler
                weibo = request.session['weibo']
                gambler.weibo = weibo
                gambler.save() 
                return myaccount(request)
        else:
            return result("Your username and password didn't match.")
    else:
        return result("Your username and password didn't match.")