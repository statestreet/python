#coding=utf-8
from django.template import Context,loader
from django.http import *
import md5,datetime,random,uuid
from handv.home.mail import *
from handv.home.models import * 

def index(request):  
    articles = Article.objects.filter(state='1')
    c = Context({'article':articles}) 
    t = loader.get_template('index.html')
    return HttpResponse(t.render(c))

def articles(request):  
    articles = Article.objects.filter(state='1',type='00')
    c = Context({'articles':articles}) 
    t = loader.get_template('articles.html')
    return HttpResponse(t.render(c))

def photos(request):  
    articles = Article.objects.filter(state='1',type='01')
    c = Context({'articles':articles}) 
    t = loader.get_template('photos.html')
    return HttpResponse(t.render(c))

def article(request,id):  
    id = int(id)
    article = Article.objects.get(id=id)
    c = Context({'article':article}) 
    t = loader.get_template('article.html')
    return HttpResponse(t.render(c))

def register(request):  
    c = Context({}) 
    t = loader.get_template('register.html')
    return HttpResponse(t.render(c))   
 
def doRegister(request):
    username = request.POST['username'].strip()
    password = request.POST['password'].strip() 
    password1 = request.POST['password1'].strip() 
    email =request.POST['email']  
    name =request.POST['name']  
    if username=='' or password=='' or password1=='' or email=='' or name=='':
        return result("请输入完整注册信息，注册的每项都是必填地...")
    if password!=password1:
        return result("两次密码对不上啊...")
    if validateEmail(email):
        u = User.objects.filter(email=email)
        if len(u)>0:
            return result("邮箱被人用过了...")
        else:
            u = User.objects.filter(username=username)
            if len(u)>0:
                return result("用户名被人用过了...")
            else:
                password = md5.new(password)
                code = str(uuid.uuid1())
                user = User(name=name,username=username,email=email,regtime=datetime.datetime.now(),password=password.hexdigest(),state='0',internal=0,code=code)
                user.save()
                html = "请点击 <a href='http://www.handv.org/confirm?code="+code+"'>'http://www.handv.org/confirm?code="+code+"'</a>进行注册确认！"
                send_mail(email,"一休和老刘的朋友注册确认",html)
                return result("去你的邮箱查查注册确认邮件吧！")
    else:
        return result("邮箱格式不对啊！")

def findback(request):  
    c = Context({}) 
    t = loader.get_template('findback.html')
    return HttpResponse(t.render(c))   
 
def doFindback(request):
    username = request.POST['username'].strip()
    email =request.POST['email']  
    if username==''  or email=='':
        return result("请输入完整注册信息，注册的每项都是必填地...")
    u = User.objects.filter(email=email,username=username)
    if len(u)>0:
        u = u[0]
        p= str(random.randint(0,6))+str(random.randint(0,6))+str(random.randint(0,6))+str(random.randint(0,6))+str(random.randint(0,6))+str(random.randint(0,6))
        password = md5.new(p)
        u.password = password.hexdigest()
        u.save()
        html = "你的新密码是‘"+p+"’  ，请点击 <a href='http://www.handv.org/login/'>http://www.handv.org/login/</a>进行登录，赶快修改你的新密码吧！"
        send_mail(email,"一休和老刘的小窝新密码",html)
        return result("新密码已经发到你的邮箱了！")
    else:
        return result("输入的信息有误啊！")
 
def result(result):
    c = Context({'result':result}) 
    t = loader.get_template('result.html')
    return HttpResponse(t.render(c)) 

def validateEmail(email):
    if len(email) > 6:
        if re.match('^[\w\.-]+@[\w\.-]+\.\w{2,4}$', email) != None:
            return 1
    return 0

def confirm(request):
    code = request.GET['code'].strip()
    u = User.objects.filter(code=code)
    u=u[0]
    u.state='1'
    u.save()
    return result("确认成功，请<a href='/login/'>登录</a>")