from django.shortcuts import render
from DailyAttendance import ormoperator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

# @login_required保证这个接口只能由登录的用户来调用
# Create your views here.
@login_required
def deep_seek(request):
    return render(request, 'DeepSeek.html')

#123