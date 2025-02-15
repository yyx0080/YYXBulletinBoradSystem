import random
from Userlogin.models import UserInfo
from Userlogin import models
#这里用来写数据库的操作,可以做到解耦        

# 从中取出当前用户的签到日期
def GetUserDailyAttendanceData(username):
    attendanceData = UserInfo.objects.filter(name=username).first().last_attendance_date # 取得用户签到日期
    if not attendanceData:
        # 如果查询结果为空,返回None
        return None
    return attendanceData

# 更新当前用户的签到日期，以及用户的积分+5~20的随机值
def UpdateUserDailyAttendanceData(username,today):
    # 更新签到日期
    UserInfo.objects.filter(name=username).update(last_attendance_date=today)
    # 更新积分
    rand_point = random.randint(5, 20)
    all_point = UserInfo.objects.filter(name=username).first().point + rand_point
    UserInfo.objects.filter(name=username).update(point=all_point)
    return rand_point