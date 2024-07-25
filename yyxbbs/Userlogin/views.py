from django.shortcuts import render,HttpResponse
from django.contrib import messages
from Userlogin import ormoperator
# Create your views here.
# 写功能函数
def index(request):
    return HttpResponse("欢迎使用YYXBBS1.0")


#登录函数
def login(req):
    #第一次访问，是get请求，所以这里把界面渲染给用户
    if req.method == "GET":
        return render(req,"login.html")
    #否则为post请求，获取用户提交的数据
    else:
        username = req.POST.get("username")
        pwd = req.POST.get("password")
        print(req.POST)
        print(username,pwd)
        #这里调用ormoperator.UserInfoCorret函数进行登录验证
        if ormoperator.UserInfoCorret(username,pwd):
            return HttpResponse("登录成功") #渲染新的成功页面，这里暂时用HttpResponse代替
        else:
            messages.error(req, '用户名或密码不正确') #使用django的消息机制显示错误信息
            return render(req,"login.html")
    

def register(request):
    if request.method == "GET":
        return render(request,"register.html")
    else:
        print(request.POST)
        #这里需要判断用户的注册条件
        #1.判断用户名长度是否符合要求
        #2.判断用户名是否在数据库中重复
        #3.判断密码是否符合要求
        #4.判断两次密码是否都一致
        username = request.POST.get("username")
        password_first = request.POST.get("password_first")
        password_second = request.POST.get("password_second")
        if len(username)>20:
            messages.error(request, '用户名长度不能超过20') #使用django的消息机制显示错误信息
            return render(request,"register.html")
        
        if ormoperator.UserInfoExist(username):
            messages.error(request, '用户名已存在')
            return render(request,"register.html")
        
        if len(password_first)<6:
            messages.error(request, '密码长度不能少于6')
            return render(request,"register.html")
        
        if password_first != password_second:
            messages.error(request, '两次密码不一致')
            return render(request,"register.html")
        #这里调用ormoperator.AddUserInfo函数进行用户注册
        ormoperator.AddUserInfo(username,password_first)
        messages.success(request, '注册成功')
        return render(request,"login.html")

        

#这个函数仅作测试使用
def addtest(request):
    ormoperator.TestAddUserInfo()
    return HttpResponse("测试数据添加成功")