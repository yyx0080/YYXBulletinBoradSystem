from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def get_person_info(request):
    # 直接使用已认证的用户对象
    user = request.user
    return render(request, 'UserInfomation.html', {
        'username': user.name, 
        'last_attendance_date': user.last_attendance_date, 
        'point': user.point
    })


# 有点多此一举了，request.user就已经包含用户信息，不需要重新查询，因为设置了AUTH_USER_MODEL = 'Userlogin.UserInfo'
# 此外考虑到如果用户未登录，那么 request.user 将是匿名用户，此时调用 user.name 可能会出错。因此，应该使用 @login_required 装饰器来保护这个视图，确保只有登录用户才能访问
# from django.shortcuts import render
# from PersonInfo import ormoperator
# # Create your views here.
# # 取得个人信息函数
# def get_person_info(request):
#     # 去数据库捞取个人信息
#     # 获取当前用户名
#     username = request.user.name
#     user = ormoperator.GetUserInfoByUsername(username)
#     # 将个人信息传递给前端
#     # <p>用户名: {{ username }}</p>
#     # <p>最近一次签到日期: {{ last_attendance_date }}</p>
#     # <p>积分: {{ point }}</p>
#     return render(request, 'UserInfomation.html', {'username': user.name, 'last_attendance_date': user.last_attendance_date, 'point': user.point})
