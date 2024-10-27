from Userlogin.models import UserInfo
from django.contrib.auth.hashers import make_password,check_password
from datetime import datetime
#这里用来写数据库的操作


#测试函数，用来添加一些测试数据进去
#测试接口
def TestAddUserInfo():
    stime = datetime.datetime.now()	#这是从数据库获取的时间，类型为datetime.datetime
    print(stime)
    UserInfo.objects.create(name = "test01",password="123456",point = 5, last_login_date = stime,login_data = stime)
    UserInfo.objects.create(name = "test02",password="123",point = 2, last_login_date = stime,login_data = stime)
    UserInfo.objects.create(name = "test03",password="1789789",point = 5,last_login_date = stime,login_data = stime)
    

def UserInfoCorret(username,pwd):
    usernamefromdb = UserInfo.objects.filter(name=username)
    if usernamefromdb:
        if usernamefromdb[0].password == pwd:
            return True
    return False

def UserInfoExist(username):
    usernamefromdb = UserInfo.objects.filter(name=username)
    if usernamefromdb:
        return True
    return False

# 判断用户的密码和用户名是否正确
def IsCorretUser(username,pwd):
    user = UserInfo.objects.filter(name=username).first()
    if user is not None and check_password(pwd,user.password):
        # 修改用户的最后一次登录时间
        user.last_login_date = datetime.now()
        user.save()
        return user
    return user

#注册用户
def AddUserInfo(username,pwd):
    encrypted_password = make_password(pwd)  # 加密密码
    UserInfo.objects.create(
        name=username,
        password=encrypted_password,
        point=0,
        last_login_date=datetime.now(),
        login_date=datetime.now()  # 如果你使用了 auto_now_add，就不需要在这里设置
    )