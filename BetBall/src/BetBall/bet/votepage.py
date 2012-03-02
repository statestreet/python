#coding=utf-8

from BetBall.bet.models import Vote, Gambler, VoteColumn, VoteDetail
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
import re
import datetime
import threading

'''
for all actions of vote
'''
votePatt = re.compile("^vote-(\w+)$")
subVotePatt = re.compile("^subVote(\d+)-(\w+)$")


def goNewVotePage(request):
    context = Context({'session':request.session})
    template = loader.get_template("new_votes.htm")
    return HttpResponse(template.render(context))

def votes(request):
    votes = Vote.objects.filter(state = '10')
    context = Context({'session':request.session,'votes':votes})
    template=loader.get_template("votes.htm")
    return HttpResponse(template.render(context))

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
            context = Context({'session':request.session,'subVotes':subVotes,"vote":vote,'type':type,'result':result})
            if args and "voteResult" in args:
                context['voteResult'] = args['voteResult']
            template=loader.get_template("voteVote.htm")
            return HttpResponse(template.render(context))
    return HttpResponse("error")

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


    
        


    