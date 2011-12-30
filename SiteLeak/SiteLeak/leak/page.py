#coding=utf-8
from django.template import Context, loader,RequestContext
from django.db.models import Q
from SiteLeak.leak.models import *
from django.http import *

def index(request):  
    c = Context({}) 
    t = loader.get_template('index.html')
    return HttpResponse(t.render(c)) 

def search(request):  
    key  = request.GET['qsearch']
    msg=''
    list= None
    if key==None or key=='':
        msg = 'please enter search key!'
    else:
        list = User.objects.filter(username__contains=key)
        if len(list)==0:
            msg='No matches result for '+key
        else:
            msg='Here are the searching result for '+key   
    c = Context({'msg':msg,'list':list}) 
    t = loader.get_template('result.html')
    return HttpResponse(t.render(c))  