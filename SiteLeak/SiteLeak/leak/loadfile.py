#coding=utf-8  
'''
Created on 2011-12-26

@author: yixiugg
'''
from SiteLeak.leak.models import User
import gc

#load from tianya
#f=open('C:/kuaipan/tianya/tianya_1.txt','r')
#for line in f:#.read().decode('gb2312').split('\n'):
#    try:
#        s = line.decode('gb2312').encode('utf-8')
#        arr =  s.split()
#        email=''
#        if len(arr)>2:
#            email=arr[2]
#        user = User(username=arr[0],password=arr[1],email=email,source='tianya')
#        user.save()
#    except:  
#        print "Error-> "+line  

#load from csdn

#for i in range(1, 1):
#    if i>9:
#        fName='0'+str(i)
#    else:
#        fName='00'+str(i)
for i in range(1, 15):
    gc.disable()
    if i>9:
        fName='0'+str(i)
    else:
        fName='00'+str(i)
    with open('/home/yixiugg/dev/db/csdn/www.csdn.net.sql.'+fName,'r') as f:
        for line in f:
            try:
                arr =  line.replace('\r','').split("#")
                user = User(username=arr[0].strip(),password=arr[1].strip(),email=arr[2].strip(),source='csdn')
                user.save()
            except:  
                print "Error-> "+line  
            del line
    gc.enable()