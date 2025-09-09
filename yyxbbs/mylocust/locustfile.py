"""
Locust测试主入口文件
通过这个文件导入所有测试用户类
"""
from .user_registration import RegistrationUser
from .user_login import LoginUser

# 可以选择性地导出特定用户类用于测试
# 例如，如果只想测试注册功能：
# __all__ = ['RegistrationUser']

# from locust import HttpUser, task, between
# import random
# import string

# class BaseUser(HttpUser):
#     wait_time = between(1, 3)  # 用户等待时间1-3秒
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.username = None
#         self.password = None
#         self.csrf_token = None
    
#     def on_start(self):
#         """每个虚拟用户启动时执行"""
#         self.get_csrf_token()
    
#     def get_csrf_token(self):
#         """获取CSRF token"""
#         response = self.client.get("/login/")
#         # 从响应中提取CSRF token（根据实际HTML结构调整）
#         if response.text:
#             # 简单示例：实际需要根据HTML结构解析
#             self.csrf_token = response.cookies.get('csrftoken', '')
    
#     def random_username(self, length=8):
#         """生成随机用户名"""
#         return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
#     def random_password(self, length=10):
#         """生成随机密码"""
#         return ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%^&*', k=length))