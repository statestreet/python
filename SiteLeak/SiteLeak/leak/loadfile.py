#coding=utf-8  
'''
Created on 2011-12-26

@author: yixiugg
'''
from SiteLeak.leak.models import User

#load from tianya
f=open('C:/kuaipan/tianya/tianya_1.txt','r')
for line in f:#.read().decode('gb2312').split('\n'):
    try:
        s = line.decode('gb2312').encode('utf-8')
        arr =  s.split()
        email=''
        if len(arr)>2:
            email=arr[2]
        user = User(username=arr[0],password=arr[1],email=email,source='tianya')
        user.save()
    except:  
        print "Error-> "+line  

#load from csdn

#for i in range(1, 28):
#    if i>9:
#        fName='0'+str(i)
#    else:
#        fName='00'+str(i)
#    f=open('C:/Documents and Settings/E511125/My Documents/Downloads/csdn/www.csdn.net.sql.'+fName,'rb')
#    for line in f.read().decode('gbk').split('\n'):
#        arr =  line.replace('\r','').split("#")
#        try:
#            user = User(username=arr[0].strip(),password=arr[1].strip(),email=arr[2].strip(),source='csdn')
#            user.save()
#        except:  
#            print "Error-> "+line  