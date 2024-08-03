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

from Userlogin import views as UserloginViews
from BoardManagement import views as BoardManagementViews
#URL和py函数的对应关系，都写在这里
urlpatterns = [
    # url -> admin.site.urls这个函数
    path('admin/', admin.site.urls),
    # 这里要注意，最后一个结尾不能有“,”否则最后一个会找不到
    path('index/', UserloginViews.index),
    path('login/',UserloginViews.login),
    path('addtest/',UserloginViews.addtest),
    path('register/',UserloginViews.register),
    path('board/',BoardManagementViews.manage_board)
]




