from django.db import models

class Gambler(models.Model):
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    balance = models.IntegerField(4)
    state = models.CharField(max_length=2)
    code = models.CharField(max_length=32)
    regtime = models.DateTimeField()
    email=models.CharField(max_length=100)
    password= models.CharField(max_length=32)
    weibo = models.CharField(max_length=32)
    weibo_nick = models.CharField(max_length=50)
    internal = models.IntegerField(1)

class Friend(models.Model):
    gambler = models.ForeignKey(Gambler,related_name='gambler')
    friend = models.ForeignKey(Gambler,related_name='friend')
    state = models.CharField(max_length=2)
    name = models.CharField(max_length=20)
    
class Lega(models.Model):
    gambler = models.ForeignKey(Gambler)
    name = models.CharField(max_length=20)
    logo = models.CharField(max_length=200,null=True)

class Wager(models.Model):
    gambler = models.ForeignKey(Gambler)
    name = models.CharField(max_length=20)
    
class Recharge(models.Model):
    gambler = models.ForeignKey(Gambler)
    amount = models.IntegerField(4)
    chargetime = models.DateTimeField()
    
class Match(models.Model):
    lega = models.ForeignKey(Lega)
    wager = models.ForeignKey(Wager)
    matchdate = models.DateField()
    matchtime = models.DateTimeField() 
    hometeam = models.CharField(max_length=50)
    awayteam = models.CharField(max_length=50)
    final = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=2)
    result = models.CharField(max_length=5,null=True)
    gettime = models.DateField()
    gambler = models.ForeignKey(Gambler)

class Group(models.Model):
    gambler = models.ForeignKey(Gambler)
    name = models.CharField(max_length=20)
    
class Member(models.Model):
    group = models.ForeignKey(Group)
    gambler = models.ForeignKey(Gambler)
    
class Transaction(models.Model):
    gambler = models.ForeignKey(Gambler)
    bettime = models.DateTimeField()
    bet = models.IntegerField(4)
    match = models.ForeignKey(Match)
    result = models.CharField(max_length=1)
    state = models.CharField(max_length=2)
    
class Position(models.Model):
    match = models.ForeignKey(Match)
    position = models.CharField(max_length=50)
    postime = models.DateTimeField()
    
class Admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    weibo = models.CharField(max_length=32,null=True)
    weibo_nick = models.CharField(max_length=50,null=True)

class Vote(models.Model):
    gambler = models.ForeignKey(Gambler)
    votedate = models.DateTimeField()
    deadline = models.DateTimeField()
    state = models.CharField(max_length=2)
    name = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    result = models.DecimalField(max_digits=5, decimal_places=2)
    memo = models.CharField(max_length=500)
    
class VoteColumn(models.Model):
    vote = models.ForeignKey(Vote)
    name = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    result = models.DecimalField(max_digits=5, decimal_places=2)
    
class VoteDetail(models.Model):
    voter = models.ForeignKey(Gambler)
    vote = models.ForeignKey(Vote)
    votecolumn = models.ForeignKey(VoteColumn)
    votetime = models.DateTimeField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    memo = models.CharField(max_length=500,null=True)
    

    
