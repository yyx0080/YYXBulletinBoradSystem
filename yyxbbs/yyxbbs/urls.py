"""
URL configuration for yyxbbs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from Userlogin import views as UserloginViews
from BoardManagement import views as BoardManagementViews
from DailyAttendance import views as DailyAttendanceViews
from PersonInfo import views as PersonInfoViews
from django.conf.urls.static import static
from django.conf import settings
#URL和py函数的对应关系，都写在这里
urlpatterns = [
    # url -> admin.site.urls这个函数
    path('admin/', admin.site.urls),
    # 这里要注意，最后一个结尾不能有“,”否则最后一个会找不到
    path('', lambda request: redirect('/login/')),
    path('index/', UserloginViews.index),
    path('login/',UserloginViews.login_view),
    path('addtest/',UserloginViews.addtest), #测试接口
    path('register/',UserloginViews.register),
    path('board/',BoardManagementViews.manage_board),
    path('RichTextSubmit/',BoardManagementViews.submit_comment),
    path('AddBoradInfoTest/',BoardManagementViews.AddBoradInfoTest), #测试接口
    path('ShowRichText/',BoardManagementViews.show_richText), #测试接口
    path('DailyAttendance/',DailyAttendanceViews.daily_attendance), # 渲染每日签到页面的接口
    path('DailyAttendanceClick/',DailyAttendanceViews.daily_attendance_click),
    path('PersonInfo/',PersonInfoViews.get_person_info)
    
]




