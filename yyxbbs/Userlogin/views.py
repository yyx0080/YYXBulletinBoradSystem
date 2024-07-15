from django.shortcuts import render,HttpResponse

# Create your views here.
# 写功能函数
def index(request):
    return HttpResponse("欢迎使用YYXBBS")
