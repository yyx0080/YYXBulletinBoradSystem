from django.shortcuts import render,HttpResponse,redirect
from BoardManagement import ormoperator
from django.http import JsonResponse
from .models import BoradInfo #这里其实是用不到的。记得注释掉
from django.core.paginator import Paginator
import datetime
import os

# Create your views here.
# 主界面，登录成功后调用这个接口
def manage_board(request):
    # 这里将数据库中的数据取出来,传给前端展示即可
    borad_info_list = ormoperator.GetBoradInfo()

    # 分页，每页显示 10 条评论
    paginator = Paginator(borad_info_list, 10)  
    page_number = request.GET.get('page')  # 从 URL 获取当前页码
    page_obj = paginator.get_page(page_number)  # 获取当前页的数据

    # 将分页对象传递给前端
    context = {'comments': page_obj}
    return render(request, 'board.html', context)
    #return HttpResponse("Manage Board")

#到时候上线网站的时候要清理掉这些测试接口，测试接口会标明测试
#测试接口
def AddBoradInfoTest(request):
    ormoperator.TestAddBoradInfo()
    return HttpResponse("添加成功")

def submit_comment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if request.user.is_authenticated:
            #获取当前用户名
            username = request.user.name
            print("name = ",username)
            #调用数据库操作,向数据库内部添加数据
            ormoperator.AddUserComment(username, content)
            #这里要返回上一层级
            return redirect('../board') #重定向到当前页面（作为刷新作用）
        else:
            return HttpResponse("请先登录")
    
    else:
        return HttpResponse("Not POST")
    

#测试富文本展示接口
#测试接口
def show_richText(request):
    # 查询 test01 用户的发言记录
    comments = BoradInfo.objects.filter(username='test07')
    # 将查询结果传递到模板中进行展示
    return render(request, 'display_comments.html', {'comments': comments})

#点赞功能
def like_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        print(comment_id)
        isCommentExist = ormoperator.AddLikePointByCommentId(comment_id)
        if isCommentExist:
            return JsonResponse({"status": "success", "new_like_count": ormoperator.GetLikePointByCommentId(comment_id)})
        else:
            return JsonResponse({"status": "error", "message": "评论不存在"})


    return JsonResponse({"status": "error", "message": "无效请求"})