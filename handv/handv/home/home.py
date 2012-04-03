'''
Created on 2012-4-3

@author: yixiugg
'''
from django.template import Context,loader
from django.http import HttpResponse

from handv.home.models import * 

def home(request):  
    articles = Article.objects.filter(state='1')
    c = Context({'article':articles}) 
    t = loader.get_template('index.html')
    return HttpResponse(t.render(c))

def articles(request):  
    articles = Article.objects.filter(state='1',type='00')
    c = Context({'articles':articles}) 
    t = loader.get_template('articles.html')
    return HttpResponse(t.render(c))

def photos(request):  
    articles = Article.objects.filter(state='1',type='01')
    c = Context({'articles':articles}) 
    t = loader.get_template('photos.html')
    return HttpResponse(t.render(c))

def article(request,id):  
    id = int(id)
    article = Article.objects.get(id=id)
    c = Context({'article':article}) 
    t = loader.get_template('article.html')
    return HttpResponse(t.render(c))
    