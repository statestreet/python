'''
Created on Apr 11, 2011

@author: e511125
'''
from django.http import HttpResponseRedirect 
from django.contrib.auth import SESSION_KEY 
from urllib import quote 
import random
from django.template import Context, loader,RequestContext
from django.db.models import Q
from django.http import *
from BetBall.bet.timer import *
from BetBall.bet.models import *  

class AuthMiddleware(object): 
    def process_request(self, request):
        #print request.path 
        if request.path == '/' or request.path == '/mybet/' or request.path == '/myaccount/': 
            gambler =  request.session.get('gambler')
            if gambler is None:
                n1 = random.randint(0,9)
                n2 = random.randint(0,9)
                result=0
                op = ''
                if n1%3==0:
                    result = n1+n2
                    op = str(n1)+'+'+str(n2)+'='
                if n1%3==1:
                    result = n1-n2
                    op = str(n1)+'-'+str(n2)+'='
                if n1%3==2:
                    result = n1*n2
                    op = str(n1)+'*'+str(n2)+'='
                request.session['result']=result
                c = Context({'op':op}) 
                t = loader.get_template('login.htm')
                return HttpResponse(t.render(c))
            else:
                pass
        else:
            pass