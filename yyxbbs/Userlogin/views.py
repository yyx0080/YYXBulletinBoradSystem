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
        return HttpResponse("登陆成功")
    
