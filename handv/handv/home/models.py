'''
Created on 2012-4-3

@author: yixiugg
'''
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    code = models.CharField(max_length=32)
    regtime = models.DateTimeField()
    email=models.CharField(max_length=100)
    password= models.CharField(max_length=32)
    weibo = models.CharField(max_length=32)
    weibo_nick = models.CharField(max_length=50)
    internal = models.IntegerField(1)
    
class Category(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=200)
    type = models.CharField(max_length=2) 
        
class Article(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    addtime = models.DateTimeField() 
    title = models.CharField(max_length=200)
    content = models.TextField(default='')
    state = models.CharField(max_length=2)
    type = models.CharField(max_length=2)
    
class Comment(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    addtime = models.DateTimeField() 
    title = models.CharField(max_length=200)
    content = models.TextField(default='')
    state = models.CharField(max_length=2)
    
class Attachment(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    addtime = models.DateTimeField()
    filepath = models.CharField(max_length=500)  
    type = models.CharField(max_length=2) 
