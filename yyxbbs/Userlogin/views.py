from django.shortcuts import render,HttpResponse

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
        print(req.POST)
        username = req.POST.get("user")
        pwd = req.POST.get("pwd")
        #这里判断条件用函数解耦合出来
        if username == "root":
            return HttpResponse("登陆成功") #渲染新的成功页面
        
        return HttpResponse(req,"login.html",{"error_msg" : "error_username" })
    

#测试bootstrap是否配置好的函数
def TestBootStrap(request):
    return render(request,"bootstraptest.html")
