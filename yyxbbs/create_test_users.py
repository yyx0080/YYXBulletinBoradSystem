import os
import django
import random
import string

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yyxbbs.settings')
django.setup()

from Userlogin.models import UserInfo
from django.contrib.auth.hashers import make_password

def create_test_users(count=100):
    """创建测试用户"""
    for i in range(count):
        username = f"testuser_{i}"
        password = f"Password123!{i}"
        
        # 检查用户是否已存在
        if not UserInfo.objects.filter(name=username).exists():
            encrypted_password = make_password(password)
            UserInfo.objects.create(
                name=username,
                password=encrypted_password,
                point=0,
                last_login_date=None,
                login_date=None,
                last_attendance_date=None
            )
            print(f"创建用户: {username}")
        else:
            print(f"用户已存在: {username}")

if __name__ == "__main__":
    create_test_users(100)
    print("测试用户创建完成")