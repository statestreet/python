#coding=utf-8  
'''
Created on 2011-12-26

@author: yixiugg
'''
from SiteLeak.leak.models import User

#f=open('/home/yixiugg/下载/tianya_1','rb')
#for line in f.read().decode('utf-8').split('\n'):
#    arr =  line.split()
#    try:
#        user = User(username=arr[0],password=arr[1],email=arr[2],source='tianya')
#        user.save()
#    except:  
#        print "Error-> "+line  

#load from csdn

for i in range(1, 28):
    if i>9:
        fName='0'+str(i)
    else:
        fName='00'+str(i)
    f=open('C:/Documents and Settings/E511125/My Documents/Downloads/csdn/www.csdn.net.sql.'+fName,'rb')
    for line in f.read().decode('gbk').split('\n'):
        arr =  line.replace('\r','').split("#")
        try:
            user = User(username=arr[0].strip(),password=arr[1].strip(),email=arr[2].strip(),source='csdn')
            user.save()
        except:  
            print "Error-> "+line  