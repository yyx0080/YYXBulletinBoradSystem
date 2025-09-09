from locust import HttpUser, task, between
import random
import string
import re

class RegistrationUser(HttpUser):
    """
    专门测试用户注册功能的Locust用户类
    """
    wait_time = between(1, 3)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csrf_token = None
        self.username = None
        self.password = None
    
    def on_start(self):
        """每个虚拟用户启动时执行"""
        self.get_csrf_token("/register/")
    
    def get_csrf_token(self, url):
        """获取CSRF token"""
        with self.client.get(url, catch_response=True) as response:
            if response.status_code == 200:
                # 尝试从HTML中提取CSRF token
                csrf_match = re.search(
                    r'name="csrfmiddlewaretoken" value="([^"]+)"', 
                    response.text
                )
                if csrf_match:
                    self.csrf_token = csrf_match.group(1)
                    return self.csrf_token
                else:
                    # 尝试从cookie获取
                    self.csrf_token = response.cookies.get('csrftoken')
                    return self.csrf_token
            return None
    
    def generate_test_username(self):
        """生成唯一的测试用户名"""
        return f"testuser_{random.randint(100000, 999999)}"
    
    def generate_test_password(self):
        """生成测试密码"""
        return f"Test@123{random.randint(100, 999)}"
    
    @task(1)
    def load_registration_page(self):
        """加载注册页面"""
        with self.client.get("/register/", catch_response=True, name="01_Load_Registration_Page") as response:
            if response.status_code == 200 and "请 注 册" in response.text:
                response.success()
                # 更新CSRF token
                self.get_csrf_token("/register/")
            else:
                response.failure(f"注册页面加载失败: {response.status_code}")
    
    @task(3)
    def perform_registration(self):
        """执行用户注册"""
        if not self.csrf_token:
            self.get_csrf_token("/register/")
        
        # 生成唯一的测试用户名和密码
        self.username = self.generate_test_username()
        self.password = self.generate_test_password()
        
        registration_data = {
            "username": self.username,
            "password_first": self.password,
            "password_second": self.password,
            "csrfmiddlewaretoken": self.csrf_token
        }
        
        with self.client.post(
            "/register/", 
            data=registration_data,
            headers={
                "Referer": f"{self.host}/register/",
                "X-CSRFToken": self.csrf_token,
                "X-Requested-With": "XMLHttpRequest"
            },
            catch_response=True,
            name="02_Perform_Registration"
        ) as response:
            # 检查注册是否成功
            if response.status_code == 200:
                if "注册成功" in response.text:
                    response.success()
                elif "用户名已存在" in response.text:
                    response.failure("注册失败 - 用户名已存在")
                    
                elif "两次密码不一致" in response.text:
                    response.failure("注册失败 - 密码不一致")
                elif "用户名长度不能超过20" in response.text:
                    response.failure("注册失败 - 用户名超长")
                elif "密码长度不能少于6" in response.text:
                    response.failure("注册失败 - 密码太短")
                else:
                    response.failure("注册失败 - 未知原因")
            elif response.status_code == 302:
                # 重定向到登录页面表示注册成功
                response.success()
            else:
                response.failure(f"注册请求失败: {response.status_code}")




# from locust import task, tag
# from .locustfile import BaseUser
# import random
# import re

# class RegistrationUser(BaseUser):
#     """测试用户注册性能"""
    
#     @task(5)
#     @tag("registration")
#     def load_registration_page(self):
#         """加载注册页面"""
#         with self.client.get("/register/", catch_response=True) as response:
#             # 检查页面是否成功加载
#             if response.status_code == 200 and "请 注 册" in response.text:
#                 response.success()
#                 # 尝试从页面提取CSRF token
#                 csrf_match = re.search(
#                     r'name="csrfmiddlewaretoken" value="([^"]+)"', 
#                     response.text
#                 )
#                 if csrf_match:
#                     self.csrf_token = csrf_match.group(1)
#             else:
#                 response.failure(f"注册页面加载失败: {response.status_code}")
    
#     @task(1)
#     @tag("registration")
#     def perform_registration(self):
#         """执行用户注册"""
#         if not self.csrf_token:
#             self.get_csrf_token()
            
#         self.username = self.random_username()
#         self.password = self.random_password()
        
#         registration_data = {
#             "username": self.username,
#             "password_first": self.password,
#             "password_second": self.password,
#             "csrfmiddlewaretoken": self.csrf_token
#         }
        
#         with self.client.post(
#             "/register/", 
#             data=registration_data,
#             headers={"Referer": f"{self.host}/register/"},
#             catch_response=True
#         ) as response:
#             # 检查注册是否成功
#             if response.status_code == 200 and "注册成功" in response.text:
#                 response.success()
#                 self.logger.info(f"成功注册用户: {self.username}")
#             elif response.status_code == 200 and "请 注 册" in response.text:
#                 # 可能是表单验证错误
#                 error_msg = "注册失败 - 表单验证错误"
#                 if "用户名已存在" in response.text:
#                     error_msg = "注册失败 - 用户名已存在"
#                 elif "两次密码不一致" in response.text:
#                     error_msg = "注册失败 - 密码不一致"
#                 response.failure(error_msg)
#             else:
#                 response.failure(f"注册请求失败: {response.status_code}")