from Userlogin.models import UserInfo



# 根据用户名取得用户信息
def GetUserInfoByUsername(username):
    userinfo = UserInfo.objects.get(name=username)
    return userinfo
