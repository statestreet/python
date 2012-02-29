#coding=utf-8

from BetBall.bet.models import Vote, Gambler, VoteColumn, VoteDetail
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
import re
import datetime

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

def voteVote(request):
    id = request.GET['id']
    if id:
        vote = Vote.objects.filter(id=id)
        if vote:
            subVotes = VoteColumn.objects.filter(vote=vote)
            if not subVotes :
                subVotes = list(subVotes).append(vote)
            context = Context({'session':request.session,'subVotes':subVotes,"vote":vote})
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

def newVote(request):
    pass


    