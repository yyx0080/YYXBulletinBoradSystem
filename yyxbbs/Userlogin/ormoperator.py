from Userlogin.models import UserInfo
import datetime
#这里用来写数据库的操作


#测试函数，用来添加一些测试数据进去
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

#注册用户
def AddUserInfo(username,pwd):
    UserInfo.objects.create(name = username,password=pwd,point = 0
                            ,last_login_date = datetime.datetime.now(),login_data = datetime.datetime.now())
