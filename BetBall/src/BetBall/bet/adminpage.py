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

def adminLogin(request):  
    m = Admin.objects.filter(username=request.POST['username'])      
    pwd = md5.new(request.POST['password'])
    pwd.digest()
    if len(m)!=0:
        if  m[0].password == pwd.hexdigest():
            request.session['gambler'] = None
            request.session['admin'] = m[0]
            lock = threading.RLock()
            lock.acquire();
            gamblers = Gambler.objects.filter(name='admin')
            admingambler = None
            if not gamblers:
                admingambler = Gambler(username='admin',name='admin',balance=0,state='00',regtime=datetime.datetime.now(),internal=1)
                admingambler.save()
            else:
                admingambler = gamblers[0]
            lock.release()
            request.session['gambler'] = admingambler
            gettime = datetime.date.today()    
            list = Match.objects.filter(gettime=gettime).order_by('state')      
            c = Context({'list':list,'session':request.session}) 
            t = loader.get_template('admin.htm')
            return HttpResponse(t.render(c))
        else:
            return result("Your username and password didn't match.")
    else:
        return result("Your username and password didn't match.")

def adminLogout(request):
    try:
        del request.session['admin']
    except KeyError:
        pass
    return result("You're logged out.")


def admin(request): 
    admin=request.session.get('admin')  
    if admin is None:
        t = loader.get_template('admin_login.htm')
        c = Context({}) 
        return HttpResponse(t.render(c))
    now = datetime.datetime.now()    
    list = Match.objects.filter(matchtime__gte=now).order_by('-state','matchtime')        
    c = Context({'list':list,'session':request.session}) 
    t = loader.get_template('admin.htm')
    return HttpResponse(t.render(c))
 
def adminresult(r):
    c = Context({'result':r}) 
    t = loader.get_template('admin_result.htm')
    return HttpResponse(t.render(c))


def openMatch(request,id): 
    id=int(id)
    match = Match.objects.get(id=id)
    match.state='1'
    match.save()
    g = Gambler.objects.filter(~Q(weibo_nick=''),~Q(weibo_nick=None)) 
    at_user=''
    for gambler in g:
        at_user+='@'+gambler.weibo_nick+' '
    #发微博吸引投注！
    status = u'亲们，又有比赛可以砸可乐拉！'+match.hometeam+'vs'+match.awayteam+u'，您别b4啊！'+SITE_URL+' '+at_user
    if client!=None:
        expires_in = request.session.get('expires_in')
        access_token = request.session.get('access_token')
        if expires_in!=None and access_token!=None:
            client.set_access_token(access_token, expires_in)
            client.post.statuses__update(status=status)
    return adminresult("Match open!")

def closeMatch(request,id):   
    id=int(id)
    match = Match.objects.get(id=id)
    match.state='0'
    match.save()
    return adminresult("Match close!")

def openGambler(request,id): 
    id=int(id)
    gambler = Gambler.objects.get(id=id)
    gambler.state='1'
    gambler.save()
    return adminresult("Gambler open!")

def closeGambler(request,id):   
    id=int(id)
    gambler = Gambler.objects.get(id=id)
    gambler.state='0'
    gambler.save()
    return adminresult("Gambler close!")

    
def opened(request):   
    admin=request.session.get('admin')
    if admin is None:
        return adminresult("You've not admin!")
    list = Match.objects.filter(state='1').order_by('-gettime')      
    c = Context({'list':list,'session':request.session}) 
    t = loader.get_template('opened.htm')
    return HttpResponse(t.render(c))
 
def viewGamblerBet(request,id): 
    admin=request.session.get('admin')
    if admin is None:
        return adminresult("You've not admin!")
    id=int(id)
    gambler = Gambler.objects.get(id=id)    
    list = Transaction.objects.filter(gambler=gambler).order_by('-bettime')       
    c = Context({'list':list,'gambler':gambler,'session':request.session}) 
    t = loader.get_template('gambler_bet.htm')
    return HttpResponse(t.render(c))

def refreshMatches(request):   
    admin=request.session.get('admin')
    if admin is None:
        return result("You've not admin!") 
    getMatches()
    return result("Get Matches again!") 

def clean(request,id):
    admin=request.session.get('admin')
    if admin is None:
        return adminresult("You've not admin!")
    id=int(id)
    transaction = Transaction.objects.get(id=id) 
    transaction.state='2'
    transaction.save()
    return adminresult("Transaction clean!") 

def settle(request,id):
    admin=request.session.get('admin')
    if admin is None:
        return adminresult("You've not admin!")
    id=int(id)
    bet = Transaction.objects.get(id=id)
    if bet.match.result is not None and bet.match.result!="":
        if bet.match.result==bet.result:
            bet.gambler.balance=( bet.gambler.balance+1)
            bet.bet=1
        else:
            bet.gambler.balance=( bet.gambler.balance-1)
            bet.bet=-1
    bet.state='1'
    bet.save()
    return adminresult("Transaction settled!")   
 
def setResult(request,id,r):
    id=int(id)
    result=int(r)
    match = Match.objects.get(id=id) 
    match.result=result
    match.save()
    bets = Transaction.objects.filter(match=match).order_by('-bettime') 
    for bet in bets:
        if bet.state!='1':
            if bet.result==r:
                bet.gambler.balance=( bet.gambler.balance+1)
                bet.bet=1
            else:
                bet.gambler.balance=( bet.gambler.balance-1)
                bet.bet=-1
            bet.gambler.save()
        bet.state='1'
        bet.save()
    return adminresult("Set result succeed!")    

def viewGambler(request):   
    admin=request.session.get('admin')
    if admin is None:
        t = loader.get_template('admin_login.htm')
        c = Context({}) 
        return HttpResponse(t.render(c))
    list = Gambler.objects.filter(~Q(username='admin')).order_by("-state") 
    c = Context({'list':list,'session':request.session}) 
    t = loader.get_template('gambler.htm')
    return HttpResponse(t.render(c))


def setGamblerVote(request,id,r): 
    id=int(id)
    r=int(r)
    gambler = Gambler.objects.get(id=id)    
    gambler.internal=r
    gambler.save()
    return adminresult("Gambler vote set!")

 
def addMatch(request):  
    gambler = request.session.get('gambler')
    t =time.strptime(request.POST['matchtime'], "%Y-%m-%d %H:%M:%S")
    y,m,d,h,M,s = t[0:6]
    matchtime=datetime.datetime(y,m,d,h,M,s)
    matchdate=datetime.date(y,m,d)
    lega=request.POST['lega'];
    legas = Lega.objects.filter(name=lega)
    if len(legas)==0:
        newlega = Lega(name=lega,gambler=gambler)
        newlega.save()
    else:
        newlega = legas[0]
    water=request.POST['water'];
    hometeam=request.POST['hometeam'];
    awayteam=request.POST['awayteam'];
    match = Match(gettime=datetime.datetime.now(),lega=newlega,matchtime=matchtime,matchdate=matchdate,hometeam=hometeam,awayteam=awayteam,state='1',final=water)
    match.save()
    return adminresult("Add match succeed!") 



def goAdminlogin(request):
    c = Context({}) 
    t = loader.get_template('admin_login.htm')
    return HttpResponse(t.render(c))
