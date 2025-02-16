from django.shortcuts import render
from PersonInfo import ormoperator
# Create your views here.
# 取得个人信息函数
def get_person_info(request):
    # 去数据库捞取个人信息
    # 获取当前用户名
    username = request.user.name
    user = ormoperator.GetUserInfoByUsername(username)
    # 将个人信息传递给前端
    # <p>用户名: {{ username }}</p>
    # <p>最近一次签到日期: {{ last_attendance_date }}</p>
    # <p>积分: {{ point }}</p>
    return render(request, 'UserInfomation.html', {'username': user.name, 'last_attendance_date': user.last_attendance_date, 'point': user.point})
