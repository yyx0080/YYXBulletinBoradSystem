from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.
#这里操作数据库
#这里的models和数据库一一对应
#这里的models其实是django框架对数据库的一个持久化

# 用户管理器
class UserInfoManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError("Users must have an username")
        user = self.model(name=name, **extra_fields)
        user.set_password(password)  # 哈希密码
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(name, password, **extra_fields)

# 用户模型
class UserInfo(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=32, unique=True)  # 确保用户名唯一
    password = models.CharField(max_length=128)  # 使用较大的字段以存储哈希后的密码
    point = models.IntegerField(default=0)  # 积分，默认为0
    last_login_date = models.DateTimeField(null=True, blank=True)  # 最后一次登录时间
    login_date = models.DateField(auto_now_add=True)  # 注册日期，自动添加日期
    last_attendance_date = models.DateField(null=True, blank=True) # 最后签到日期


    is_active = models.BooleanField(default=True)  # 用户是否激活
    is_staff = models.BooleanField(default=False)  # 是否为管理员

    # 指定用于身份验证的字段
    USERNAME_FIELD = 'name'  # 用户的唯一标识符
    REQUIRED_FIELDS = []  # 如果需要其他字段，可以在这里添加

    objects = UserInfoManager()  # 指定用户管理器

    def __str__(self):
        return self.name

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


#留言表
class BoradInfo(models.Model):
    username = models.CharField(max_length=32) #留言的用户
    content = models.CharField(max_length=800) #最多写800字小作文
    board_data = models.DateTimeField() #留言的时间





