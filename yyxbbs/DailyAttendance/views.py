from django.shortcuts import render
from DailyAttendance import ormoperator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from Ranking.ormoperator import clear_ranking_cache
from PersonInfo.ormoperator import clear_user_cache_by_username


# @login_required保证这个接口只能由登录的用户来调用
# Create your views here.
@login_required
def daily_attendance(request):
    return render(request, 'DailyAttendance.html')

# 用户点击每日签到按钮
@login_required
def daily_attendance_click(request):
    today = timezone.now().date()
    username = request.user.name
    # 检查用户是否已经签到过了，就是从数据库中捞取用户签到的日期，判断是不是今天
    curDailyAttendanceData = ormoperator.GetUserDailyAttendanceData(username)

    if curDailyAttendanceData == today:
        messages.error(request, "今天你已经签到过了！")
        return render(request, 'DailyAttendance.html')
    else:
        # 签到成功，更新数据库
        point = ormoperator.UpdateUserDailyAttendanceData(username, today)
        # 清除排行榜缓存
        clear_ranking_cache()
        # 清除用户信息缓存
        clear_user_cache_by_username(username)
        messages.success(request, "签到成功，获得积分：" + str(point))
    return render(request, 'DailyAttendance.html')

    