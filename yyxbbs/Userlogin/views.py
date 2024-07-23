from django.shortcuts import render,HttpResponse
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
        username = req.POST.get("user")
        pwd = req.POST.get("pwd")
        #这里调用ormoperator.UserInfoCorret函数进行登录验证
        if ormoperator.UserInfoCorret(username,pwd):
            return HttpResponse("登录成功") #渲染新的成功页面
        else:
            return HttpResponse("用户名或者密码错误")
    

#这个函数仅作测试使用
def addtest(request):
    ormoperator.TestAddUserInfo()
    return HttpResponse("测试数据添加成功")