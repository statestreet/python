#coding=utf-8  
'''
Created on 2011-12-26

@author: yixiugg
'''
from SiteLeak.leak.models import User

f=open('/home/yixiugg/下载/tianya_1','rb')
for line in f.read().decode('utf-8').split('\n'):
    arr =  line.split()
    try:
        user = User(username=arr[0],password=arr[1],email=arr[2],source='tianya')
        user.save()
    except:  
        print "Error-> "+line  
