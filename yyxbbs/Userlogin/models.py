from django.db import models

# Create your models here.
#这里操作数据库
#这里的models和数据库一一对应
#这里的models其实是django框架对数据库的一个持久化

#用户表
class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=20)
    point = models.IntegerField(default=0) #积分，默认为0
    last_login_date = models.DateTimeField() #最后一次登录时间
    login_data = models.DateField() #注册日期


#留言表
class BoradInfo(models.Model):
    username = models.CharField(max_length=32) #留言的用户
    content = models.CharField(max_length=800) #最多写800字小作文
    board_data = models.DateTimeField() #留言的时间





