from django.shortcuts import render,HttpResponse
from BoardManagement import ormoperator
from django.http import JsonResponse
from .models import BoradInfo #这里其实是用不到的。记得注释掉
import datetime
import os


# Create your views here.
def manage_board(request):
    return HttpResponse("Manage Board")

#到时候上线网站的时候要清理掉这些测试接口，测试接口会标明测试
#测试接口
def AddBoradInfoTest(request):
    ormoperator.TestAddBoradInfo()
    return HttpResponse("添加成功")


#测试富文本写入
#测试接口
def submit_comment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        content = request.POST.get('content')
        image = request.FILES.get('image')


        BoradInfo.objects.create(
            username=username,
            content=content,
            board_date=datetime.date.today(),
            like_point=0,
            type=1 if image else 0
        )

        return JsonResponse({'status': 'success'})
    return render(request, 'submit_commit.html')

#测试富文本展示接口
#测试接口
def show_richText(request):
    # 查询 test01 用户的发言记录
    comments = BoradInfo.objects.filter(username='test07')
    # 将查询结果传递到模板中进行展示
    return render(request, 'display_comments.html', {'comments': comments})
