'''
Created on 2011-3-22

@author: yixiugg
'''
#coding=utf-8  
import threading
import datetime
from BetBall.bet.MyHTMLParser import MyHtmlParser
from BetBall.bet.models import *  

class BetTimer():
    '''
    classdocs
    '''

def getMatches():
    parser = MyHtmlParser()
    list = parser.getListFromUrl("http://odds.sports.sina.com.cn/odds/")

    for p in list:
        data = p.split(",")
        print p
        result=''
        matchdate=datetime.date.today()
        matchtime = datetime.datetime.now()
        for i in range(len(data)):
            s =data[i]
            if s=='\xe7\x9b\x98\xe8\xb7\xaf':#decode Chinese
                bs=data[i-1]
                try:
                    if bs.index("-") != -1:
                        result = bs
                except ValueError:
                    print 'no score'
                matchd=data[i+1].split(" ")[0]
                matcht=data[i+1].split(" ")[1]
                hour=matcht.split(":")[0]
                minute=matcht.split(":")[1]
                month = matchd.split("-")[0]
                date =  matchd.split("-")[1]
                today = datetime.date.today()
                matchdate =datetime.date(int(today.strftime("%Y")[0:4]),int(month),int(date))  
                matchtime = datetime.datetime(int(today.strftime("%Y")[0:4]),int(month),int(date),int(hour),int(minute))  
                break
        lega=data[0]
        hometeam=data[2].split("vs")[0]
        awayteam=data[2].split("vs")[1]
        final= data[4]
        legas = Lega.objects.filter(name=lega)
        gamblers = Gambler.objects.filter(name='admin')
        admingambler=None
        if len(gamblers)==0:
            admingambler = Gambler(username='admin',name='admin',balance=0,state='00',regtime=datetime.datetime.now(),internal=1)
            admingambler.save()
        else:
            admingambler= gamblers[0]
        if len(legas)==0:
            newlega = Lega(name=lega,gambler=admingambler)
            newlega.save()
        else:
            newlega = legas[0]
        matchs = Match.objects.filter(gambler=admingambler,lega=newlega,matchdate=matchdate,hometeam=hometeam,awayteam=awayteam)
        wagers = Wager.objects.filter(gambler=admingambler,name='coke')
        wager = None
        if len(wagers)==0:
            wager = Wager(gambler=admingambler,name='coke')
            wager.save()
        else:
            wager= wagers[0]
        
        if len(matchs)==0:
            match = Match(gambler=admingambler,wager=wager,gettime=datetime.datetime.now(),lega=newlega,matchtime=matchtime,matchdate=matchdate,hometeam=hometeam,awayteam=awayteam,final=final,state='0',result=result)
            match.save()
        else:
            match = matchs[0]
            match.matchtime=matchtime
            match.gettime=datetime.datetime.now()
            match.final=final
            #ignore result if result has been updated
            if match.result == None:
                match.result=result
            match.save()
        print lega,' - ' ,matchtime,' - ' ,hometeam,' - ' ,awayteam,' - ' ,final,' - ' ,result
    global t        #Notice: use global variable!
    t = threading.Timer(3600.0, getMatches)
    t.start()

t = threading.Timer(3600.0, getMatches)
t.start()


