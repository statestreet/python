#coding=utf-8

from BetBall.bet.models import Vote, Gambler, VoteColumn, VoteDetail
from django.db import transaction
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
import adminpage
import datetime
import page
import re
import threading
import logging
from django.db.models import Q
'''
for all actions of vote
'''
votePatt = re.compile("^vote-(\w+)$")
subVotePatt = re.compile("^subVote(\d+)-(\w+)$")
delSubVotePatt = re.compile("^del-(\d+)$")
logger = logging.getLogger(__name__)

def response(template_name,**kargs):
    try:
        template = loader.get_template(template_name)
        if template:
            logger.info('find template : %s' % template)
            context = Context(kargs)
            return HttpResponse(template.render(context))
    except Exception, e:
            print e
    logger.info('no template : %s dispatch it for content' % template_name)
    return HttpResponse(template_name) 

def interceptor(func):
    logger.info('interceptor function : %s ' % func.__name__);
    def wapper(request,*args,**kargs):
        if 'gambler' in request.session and request.session['gambler']:
            try:
                response =  func(request,*args,**kargs)
                return response
            except Exception,e:
                print e
                return HttpResponse("error")
        else:
            return page.gologin(request)
    return wapper


def adminInterceptor(func):
    def wapper(request,*args,**kargs):
        if 'admin' in request.session and request.session['admin']:
            try:
                response =  func(request,*args,**kargs)
                return response
            except Exception,e:
                print e
                return HttpResponse("error")
        else:
            return adminpage.goAdminlogin(request)
    
    return wapper

def dispatch(func):
    def wrapper(request):
        session = request.session
        args = {}
        args['session'] = session
        args['request'] = request
        for k,v in request.GET.items():
            args[k] = v
        for k,v in request.POST.items():
            args[k] = v
        return func(**args)
    return wrapper
        

@adminInterceptor
def goNewVotePage(request):
    context = Context({'session':request.session})
    template = loader.get_template("new_votes.htm")
    return HttpResponse(template.render(context))

@interceptor
def votes(request):
    votes = Vote.objects.filter(state = '10',deadline__gte = datetime.date(datetime.datetime.now().year,
                                                                           datetime.datetime.now().month,
                                                                           datetime.datetime.now().day))
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

@adminInterceptor
@transaction.commit_on_success  
def saveOrUpdateVote(request):
    result = 'success'
    voteMap = {}
    subVoteMap = {}
    for k,v in request.POST.items():
        m = re.match(delSubVotePatt,k)
        if m and v:
            print v
            subVote = VoteColumn.objects.get(id=v)
            subVote.delete()
            print("del subVote with id: " + v)
            continue
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
    type = 'add'
    if vote.id:
        type = 'update'
        if Vote.objects.get(id = vote.id).gambler.id  != request.session['gambler'].id:
            raise Exception('can not edit !')
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
    if type == 'update':
        template = loader.get_template("editVote.htm")
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
        reflashVoteResult(vote)
        return voteVote(request,{'voteResult':'success'})
    finally:
        lock.release()
        
    return HttpResponse("error")  

@adminInterceptor
def myVotes(request,**kargs):
    gambler = 'gambler' in request.session and request.session['gambler']
    votes = Vote.objects.filter(gambler=gambler)
    context = Context({"votes":votes,'session':request.session})
    result = 'result' in kargs and kargs['result']
    if result : context['result'] = result
    template = loader.get_template("myVotes.htm")
    return HttpResponse(template.render(context))

@adminInterceptor
def viewVote(request):
    allVoter = set([voter.name for voter in Gambler.objects.filter(~Q(username='admin'),internal=1)]);
    voteId = request.GET['id']
    vote = Vote.objects.get(id=voteId)
    subVotes = VoteColumn.objects.filter(vote=vote)
    voted = set([voteDetail.voter.name for voteDetail in VoteDetail.objects.filter(vote=vote,votecolumn=subVotes[0])])
    nonVoted = allVoter - voted
    context = Context({'session':request.session,'subVotes':subVotes,
                       'voted':','.join(voted),'nonVoted':','.join(nonVoted),'vote':vote})
    template = loader.get_template("viewVote.htm")
    return HttpResponse(template.render(context))

@adminInterceptor
@transaction.commit_on_success  
def delVote(request):
    result = ''
    gambler = 'gambler' in request.session and request.session['gambler']
    id ='id' in request.GET and request.GET['id']
    vote = Vote.objects.get(id=id)
    if vote and vote.gambler.id == gambler.id:
        vote.delete()
        result = 'success'
    else:
        result = 'Delete failed'
    return myVotes(request,result=result)

@adminInterceptor
@dispatch
def voteDetail(id,**kargs):
    vote = Vote.objects.get(id = id)
    voted = set([voteDetail.voter for voteDetail in VoteDetail.objects.filter(vote=vote)])
    return response("vote_detail.htm",voted=voted,vote=vote)

@adminInterceptor
@dispatch
def delVoter(id,voteId,**kargs):
    voter = Gambler.objects.get(id=id)
    vote  = Vote.objects.get(id = voteId)
    if voter and vote:
        VoteDetail.objects.filter(voter = voter,vote = vote).delete()
        reflashVoteResult(vote)
        return response("success")
    else :
        return response("falied")
    

@adminInterceptor
def goEditVote(request):
    id = request.GET['id']
    vote = Vote.objects.get(id=id)
    gambler = 'gambler' in request.session and request.session['gambler']
    if vote and vote.gambler.id == gambler.id:
        subVotes = VoteColumn.objects.filter(vote=vote)
        context = Context({'session':request.session,'vote':vote,'subVotes':subVotes})
        template = loader.get_template("editVote.htm");
        if isVoted(id):
            template = loader.get_template("editDeadline.htm")
        return HttpResponse(template.render(context));
    else:
        return HttpResponse('error') 

  
def isVoted(id):
    vote = Vote.objects.get(id=id)
    voteDetails = VoteDetail.objects.filter(vote = vote)
    if len(voteDetails) == 0:
        return False
    else :
        return True
    
def reflashVoteResult(vote):
    vote.result = 0
    subVotes = VoteColumn.objects.filter(vote = vote)
    for subVote in subVotes:
        sumScore = 0;
        voteDetails =  VoteDetail.objects.filter(vote=vote,votecolumn=subVote)
        sumVoter = len(voteDetails)
        if not sumVoter :
            subVote.result = sumScore
        else :
            for voteDetail in voteDetails:
                sumScore += voteDetail.score
                subVote.result = sumScore/sumVoter
        vote.result += subVote.result
        subVote.save()
    vote.save() 
        

    
    
    


    