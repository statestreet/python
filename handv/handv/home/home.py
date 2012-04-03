'''
Created on 2012-4-3

@author: yixiugg
'''
from django.template import Context,loader
from django.http import HttpResponse
def home(request):  
    c = Context({'session':request.session}) 
    t = loader.get_template('index.html')
    return HttpResponse(t.render(c))
    