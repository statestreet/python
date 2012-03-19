from BetBall.bet.adminpage import *
from BetBall.bet.page import *
from BetBall.bet.votepage import goNewVotePage, saveOrUpdateVote, votes, \
    voteVote, vote, myVotes, viewVote, delVote, goEditVote, isVoted, voteDetail, \
    delVoter
from BetBall.bet.weibopage import *
from django.conf.urls.defaults import *
import os
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^BetBall/', include('BetBall.foo.urls')),
     (r'^$',  listTodayMatches),     
     (r'^matches/', listTodayMatches),
     (r'^opened/', opened),
     (r'^viewMatches/(?P<year>\d{4})-(?P<month>\d{2})-(?P<date>\d{2})/$', viewMatches),
     (r'^allmatches/', listTodayAllMatches),
     (r'^viewGambler/', viewGambler),
     (r'^admin/', admin),
     (r'^lega/(\w+)/$', lega),
     (r'^viewLega/', viewLega),
     (r'^adminLogout/', adminLogout),
     (r'^bet/(\d{1,10})/(\d{1,10})/$', betMatch),
     (r'^setResult/(\d{1,10})/(\d{1,10})/$', setResult),
     (r'^setGamblerVote/(\d{1,10})/(\d{1,10})/$', setGamblerVote),
     (r'^openMatch/(\d{1,10})/$', openMatch),
     (r'^closeMatch/(\d{1,10})/$', closeMatch),
     (r'^openGambler/(\d{1,10})/$', openGambler),
     (r'^closeGambler/(\d{1,10})/$', closeGambler),
     (r'^viewGamblerBet/(\d{1,10})/$', viewGamblerBet),
     (r'^viewMatchBets/(\d{1,10})/$', viewMatchBets),
     (r'^matchBets/(\d{1,10})/$', matchBets),
     (r'^clean/(\d{1,10})/$', clean),
     (r'^settle/(\d{1,10})/$', settle),
     (r'^cancelBet/(\d{1,10})/$', cancelBet),
     (r'^viewUser/(\d{1,10})/$', viewUser),
     (r'^addFriend/(\d{1,10})/$', addFriend),
     (r'^search/', search),
     (r'^myfriends/', myfriends),
     (r'^register/', register),
     (r'^gologin/', gologin),
     (r'^saveRegister/', saveRegister),
     (r'^adminLogin/', adminLogin),
     (r'^weiboLoginBack/', weiboLoginBack),
     (r'^weiboLogin/', weiboLogin),
     (r'^addMatch/', addMatch),
     (r'^login/', login),
     (r'^recharge/', recharge),
     (r'^logout/', logout),
     (r'^myaccount/', myaccount),
     (r'^updateAccount/', updateAccount),
     (r'^mybet/', mybet),
     (r'^bind/', bind),
     (r'^getPassword/', getPassword),
     (r'^getUsername/', getUsername),
     (r'^verifyImg/', verifyImg),
     (r'^refreshMatches/', refreshMatches),
     (r'^newVote/',goNewVotePage),
     (r'^saveOrUpdateVote/',saveOrUpdateVote),
     (r'^allVotes/',votes),
     (r'^voteVote',voteVote),
     (r'^vote/',vote),
     (r'^myVotes/',myVotes),
     (r'^viewVote',viewVote),
     (r'^delVote',delVote),
     (r'^goEditVote',goEditVote),
     (r'^voted',isVoted),
     (r'^voteDetail',voteDetail),
     (r'^deleteVoter',delVoter),
     (r'^image/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(globals()["__file__"]) + '/image'}),
     (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(globals()["__file__"]) + '/html/files'})
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
