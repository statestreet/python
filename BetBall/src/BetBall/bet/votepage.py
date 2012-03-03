#coding=utf-8

from BetBall.bet.models import Vote, Gambler, VoteColumn, VoteDetail
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.db import transaction
import re
import datetime
import threading

'''
for all actions of vote
'''
votePatt = re.compile("^vote-(\w+)$")
subVotePatt = re.compile("^subVote(\d+)-(\w+)$")


def interceptor(func):
    def wapper(request,*args,**kargs):
        if 'gambler' in request.session and request.session['gambler']:
            try:
                sid = transaction.savepoint()
                response =  func(request,*args,**kargs)
                return response
            except Exception,e:
                print e
                return HttpResponse("error")
        else:
            return HttpResponse("please login in!")
    
    return wapper
            

@interceptor
def goNewVotePage(request):
    context = Context({'session':request.session})
    template = loader.get_template("new_votes.htm")
    return HttpResponse(template.render(context))

@interceptor
def votes(request):
    votes = Vote.objects.filter(state = '10')
    context = Context({'session':request.session,'votes':votes})
    template=loader.get_template("votes.htm")
    return HttpResponse(template.render(context))

@interceptor
def voteVote(request,args = {}):
    id = 'id' in request.POST and request.POST['id'] or 'id' in request.GET and request.GET['id']
    voter = 'gambler' in request.session and request.session['gambler']
    if id and voter:
        vote = Vote.objects.get(id=id)
        if vote:
            subVotes = VoteColumn.objects.filter(vote=vote)
            type = 'update'
            result = 0
            if len(VoteDetail.objects.filter(vote=vote,voter=voter)) != 0:
                for subVote in subVotes:
                    voteDetails = VoteDetail.objects.filter(vote=vote,voter=voter,votecolumn=subVote)
                    voteDetail = voteDetails and voteDetails[0]
                    if voteDetail:
                        subVote.result = voteDetail.score
                        result += subVote.result
            else :
                for subVote in subVotes:
                    subVote.result = 0
            context = Context({'session':request.session,'subVotes':subVotes,"vote":vote,'type':type,'result':result})
            if args and "voteResult" in args:
                context['voteResult'] = args['voteResult']
            template=loader.get_template("voteVote.htm")
            return HttpResponse(template.render(context))
    return HttpResponse("error")

@interceptor
@transaction.commit_on_success  
def saveOrUpdateVote(request):
    result = 'success'
    voteMap = {}
    subVoteMap = {}
    for k,v in request.POST.items():
        m = re.match(votePatt,k)
        if m and v:
            voteMap[m.group(1)] = v.strip()
            continue
        m = re.match(subVotePatt,k)
        if m and v:
            count = m.group(1)
            key = m.group(2)
            subVote = count in subVoteMap and subVoteMap[count] or {}
            subVote[key] = v.strip()
            subVoteMap[count] = subVote
    vote = Vote(**voteMap)
    vote.votedate = datetime.datetime.now()
    vote.gambler = request.session['gambler']
    vote.result = vote.result or 0
    vote.save()
    for v in subVoteMap.values():
        voteColumn = VoteColumn(**v)
        voteColumn.vote = vote
        voteColumn.result = voteColumn.result or 0
        voteColumn.save()
        
    context = Context({'vote':vote,'session':request.session,'result':result})
    template = loader.get_template("new_votes.htm")
    return HttpResponse(template.render(context))

@interceptor
@transaction.commit_on_success  
def vote(request):
    id = 'id' in request.POST and request.POST['id'] or 'id' in request.GET and request.GET['id']
    if not id :
        return HttpResponse("error")  
    lock = threading.RLock()
    lock.acquire()
    try:
        vote = id and Vote.objects.get(id = id)
        voter = request.session['gambler']
        subVotes = VoteColumn.objects.filter(vote=vote).order_by('vote')
        for subVote in subVotes:
            subResult = request.POST['subVote%s-result' % subVote.id]
            voteDetails =  VoteDetail.objects.filter(vote=vote,votecolumn=subVote,voter=voter)
            voteDetail = voteDetails and voteDetails[0] or VoteDetail(
                        vote=vote,votecolumn=subVote,voter=voter,votetime=datetime.datetime.now())
            voteDetail.score = subResult
            voteDetail.save()
        sumScore = 0
        sumVoter = 0
        vote.result = 0
        for subVote in subVotes:
            sumScore = 0;
            voteDetails =  VoteDetail.objects.filter(vote=vote,votecolumn=subVote)
            sumVoter = len(voteDetails)
            for voteDetail in voteDetails:
                sumScore += voteDetail.score
            subVote.result = sumScore/sumVoter
            vote.result += subVote.result
            subVote.save()
        vote.save() 
        return voteVote(request,{'voteResult':'success'})
    finally:
        lock.release()
        
    return HttpResponse("error")  

@interceptor
def myVotes(request,**kargs):
    gambler = 'gambler' in request.session and request.session['gambler']
    votes = Vote.objects.filter(gambler=gambler)
    context = Context({"votes":votes,'session':request.session})
    result = 'result' in kargs and kargs['result']
    if result : context['result'] = result
    template = loader.get_template("myVotes.htm")
    return HttpResponse(template.render(context))

def viewVote(request):
    allVoter = set([voter.username for voter in Gambler.objects.all()]);
    voteId = request.GET['id']
    vote = Vote.objects.get(id=voteId)
    subVotes = VoteColumn.objects.filter(vote=vote)
    voted = set([voteDetail.voter.username for voteDetail in VoteDetail.objects.filter(vote=vote,votecolumn=subVotes[0])])
    nonVoted = allVoter - voted
    context = Context({'session':request.session,'subVotes':subVotes,
                       'voted':','.join(voted),'nonVoted':','.join(nonVoted),'vote':vote})
    template = loader.get_template("viewVote.htm")
    return HttpResponse(template.render(context))

@interceptor
def delVote(request):
    result = ''
    gambler = 'gambler' in request.session and request.session['gambler']
    id ='id' in request.GET and request.GET['id']
    vote = Vote.objects.get(id=id)
    if vote and vote.gambler.username == gambler.username:
        vote.delete()
        result = 'success'
    else:
        result = 'Delete failed'
    
    return myVotes(request,result=result)
        

    
    
    


    