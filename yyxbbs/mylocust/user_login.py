from locust import HttpUser, task, between
import random
import re

class LoginUser(HttpUser):
    """
    专门测试用户登录功能的Locust用户类
    """
    wait_time = between(1, 3)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csrf_token = None
    
    def on_start(self):
        """每个虚拟用户启动时执行"""
        self.get_csrf_token("/login/")
    
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
                    # print(f"从 HTML 获取 CSRF token: {self.csrf_token}")
                    return self.csrf_token
                else:
                    # 尝试从cookie获取
                    self.csrf_token = response.cookies.get('csrftoken')
                    # print(f"从 Cookie 获取 CSRF token: {self.csrf_token}")
                    return self.csrf_token
            return None
    
    @task
    def login_performance(self):
        """加载登录页面"""
        with self.client.get("/login/", catch_response=True, name="01_Load_Login_Page") as response:
            if response.status_code == 200 and "请 登 录" in response.text:
                response.success()
                # 更新CSRF token
                self.get_csrf_token("/login/")
            else:
                response.failure(f"登录页面加载失败: {response.status_code}")
        """执行用户登录"""
        # print(self.csrf_token)
        self.get_csrf_token("/login/")
        # if not self.csrf_token:
        #     self.get_csrf_token("/login/")
        #     print("111", self.csrf_token)
        # 使用预定义的测试用户
        user_id = random.randint(0, 99)
        username = f"testuser_{user_id}"
        password = f"Password123!{user_id}"
        
        login_data = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": self.csrf_token
        }
        
        with self.client.post(
            "/login/", 
            data=login_data,
            headers={
                "Referer": f"{self.host}/login/",
                # "X-CSRFToken": self.csrf_token,
                "X-CSRFToken": self.csrf_token,
                "X-Requested-With": "XMLHttpRequest",
            },
            allow_redirects=False,
            catch_response=True,
            name="02_Perform_Login"
        ) as _response:
            # print(f"响应类型: {type(_response)}")
            # print(f"响应状态码: {_response.status_code}")
            # print(f"响应内容: {_response.text}")
            # 检查登录是否成功
            if _response.status_code == 302:
                # 重定向到其他页面表示登录成功
                if "board" in _response.headers.get("Location", ""):
                    _response.success()
                else:
                    _response.failure("登录失败 - 重定向到未知页面")
            elif _response.status_code == 200:
                if "用户名或密码不正确" in _response.text:
                    _response.failure("登录失败 - 用户名或密码不正确")
                else:
                    _response.failure("登录失败 - 未知原因")
            else:
                _response.failure(f"登录请求失败: {_response.status_code}")

    # @task(1)
    # def load_login_page(self):
    #     """加载登录页面"""
    #     with self.client.get("/login/", catch_response=True, name="01_Load_Login_Page") as response:
    #         if response.status_code == 200 and "请 登 录" in response.text:
    #             response.success()
    #             # 更新CSRF token
    #             self.get_csrf_token("/login/")
    #         else:
    #             response.failure(f"登录页面加载失败: {response.status_code}")
    
    # @task(3)
    # def perform_login(self):
    #     """执行用户登录"""
    #     print(self.csrf_token)
    #     if not self.csrf_token:
    #         self.get_csrf_token("/login/")
    #         print("111", self.csrf_token)
    #     # 使用预定义的测试用户
    #     username = f"testuser_{random.randint(0, 99)}"
    #     password = f"Password123!{random.randint(0, 99)}"
        
    #     login_data = {
    #         "username": username,
    #         "password": password,
    #         "csrfmiddlewaretoken": self.csrf_token
    #     }
        
    #     with self.client.post(
    #         "/login/", 
    #         data=login_data,
    #         headers={
    #             "Referer": f"{self.host}/login/",
    #             "X-CSRFToken": self.csrf_token
    #             # "X-CSRFToken": self.csrf_token,
    #             # "X-Requested-With": "XMLHttpRequest"
    #         },
    #         catch_response=True,
    #         name="02_Perform_Login"
    #     ) as response:
    #         # 检查登录是否成功
    #         if response.status_code == 302:
    #             # 重定向到其他页面表示登录成功
    #             if "board" in response.headers.get("Location", ""):
    #                 response.success()
    #             else:
    #                 response.failure("登录失败 - 重定向到未知页面")
    #         elif response.status_code == 200:
    #             if "用户名或密码不正确" in response.text:
    #                 response.failure("登录失败 - 用户名或密码不正确")
    #             else:
    #                 response.failure("登录失败 - 未知原因")
    #         else:
    #             response.failure(f"登录请求失败: {response.status_code}")


# from locust import task, tag
# from .locustfile import BaseUser
# import re
# import random

# class LoginUser(BaseUser):
#     """测试用户登录性能"""
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # 预创建测试用户
#         self.test_users = [
#             {"username": f"testuser_{i}", "password": f"Password123!{i}"}
#             for i in range(100)  # 创建100个测试用户
#         ]
    
#     @task(3)
#     @tag("login")
#     def load_login_page(self):
#         """加载登录页面"""
#         with self.client.get("/login/", catch_response=True) as response:
#             if response.status_code == 200 and "请 登 录" in response.text:
#                 response.success()
#                 # 尝试从页面提取CSRF token
#                 csrf_match = re.search(
#                     r'name="csrfmiddlewaretoken" value="([^"]+)"', 
#                     response.text
#                 )
#                 if csrf_match:
#                     self.csrf_token = csrf_match.group(1)
#             else:
#                 response.failure(f"登录页面加载失败: {response.status_code}")
    
#     @task(1)
#     @tag("login")
#     def perform_login(self):
#         """执行用户登录"""
#         if not self.csrf_token:
#             self.get_csrf_token()
            
#         # 随机选择一个测试用户
#         user = random.choice(self.test_users)
        
#         login_data = {
#             "username": user["username"],
#             "password": user["password"],
#             "csrfmiddlewaretoken": self.csrf_token
#         }
        
#         with self.client.post(
#             "/login/", 
#             data=login_data,
#             headers={"Referer": f"{self.host}/login/"},
#             catch_response=True
#         ) as response:
#             # 检查登录是否成功
#             if response.status_code == 302 and "board" in response.headers.get("Location", ""):
#                 response.success()
#                 self.logger.info(f"成功登录用户: {user['username']}")
#             elif response.status_code == 200 and "用户名或密码不正确" in response.text:
#                 response.failure("登录失败 - 用户名或密码不正确")
#             else:
#                 response.failure(f"登录请求失败: {response.status_code}")