from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from .ormoperator import (
    get_user_profile_by_username, get_user_comments_by_username, 
    get_user_stats_by_username, get_user_ranks_by_username, 
    clear_user_cache_by_username, search_users_by_name,
    clear_user_cache_by_id
)
from Userlogin.models import UserInfo
import urllib.parse

# @login_required
# def get_person_info(request):
#     # 直接使用已认证的用户对象
#     user = request.user
#     return render(request, 'UserInfomation.html', {
#         'username': user.name, 
#         'last_attendance_date': user.last_attendance_date, 
#         'point': user.point
#     })


# 有点多此一举了，request.user就已经包含用户信息，不需要重新查询，因为设置了AUTH_USER_MODEL = 'Userlogin.UserInfo'
# 此外考虑到如果用户未登录，那么 request.user 将是匿名用户，此时调用 user.name 可能会出错。因此，应该使用 @login_required 装饰器来保护这个视图，确保只有登录用户才能访问
# from django.shortcuts import render
# from PersonInfo import ormoperator
# # Create your views here.
# # 取得个人信息函数
# def get_person_info(request):
#     # 去数据库捞取个人信息
#     # 获取当前用户名
#     username = request.user.name
#     user = ormoperator.GetUserInfoByUsername(username)
#     # 将个人信息传递给前端
#     # <p>用户名: {{ username }}</p>
#     # <p>最近一次签到日期: {{ last_attendance_date }}</p>
#     # <p>积分: {{ point }}</p>
#     return render(request, 'UserInfomation.html', {'username': user.name, 'last_attendance_date': user.last_attendance_date, 'point': user.point})

# 个人信息页大更新
@login_required
def get_person_info(request):
    """当前登录用户的个人信息页"""
    user = request.user
    
    # 使用ORM操作获取数据
    profile = get_user_profile_by_username(user.name)
    user_ranks = get_user_ranks_by_username(user.name)
    stats = get_user_stats_by_username(user.name)
    
    # 获取当前页的留言
    page = request.GET.get('page', 1)
    tab = request.GET.get('tab', 'info')
    comments_data = get_user_comments_by_username(user.name, page=page)
    
    context = {
        'user': user,
        'profile': profile,
        'user_ranks': user_ranks,
        'stats': stats,
        'comments': comments_data['comments'] if comments_data else [],
        'pagination': {
            'has_previous': comments_data['has_previous'] if comments_data else False,
            'has_next': comments_data['has_next'] if comments_data else False,
            'current_page': comments_data['current_page'] if comments_data else 1,
            'total_pages': comments_data['total_pages'] if comments_data else 1,
        } if comments_data else {},
        'active_tab': tab,
        'is_own_profile': True,  # 标记是自己的页面
    }
    
    return render(request, 'UserInfomation.html', context)

def public_user_info(request, username):
    """公开用户信息页"""
    # URL解码用户名（处理特殊字符）
    try:
        username = urllib.parse.unquote(username)
    except:
        pass
    
    # 获取用户基本信息
    profile = get_user_profile_by_username(username)
    if not profile:
        raise Http404("用户不存在")
    
    # 获取用户数据
    user_ranks = get_user_ranks_by_username(username)
    stats = get_user_stats_by_username(username)
    
    # 获取当前页的留言
    page = request.GET.get('page', 1)
    tab = request.GET.get('tab', 'info')
    comments_data = get_user_comments_by_username(username, page=page)
    
    # 检查是否是查看自己的页面
    is_own_profile = request.user.is_authenticated and request.user.name == username
    
    context = {
        'profile': profile,
        'user_ranks': user_ranks,
        'stats': stats,
        'comments': comments_data['comments'] if comments_data else [],
        'pagination': {
            'has_previous': comments_data['has_previous'] if comments_data else False,
            'has_next': comments_data['has_next'] if comments_data else False,
            'current_page': comments_data['current_page'] if comments_data else 1,
            'total_pages': comments_data['total_pages'] if comments_data else 1,
        } if comments_data else {},
        'active_tab': tab,
        'is_own_profile': is_own_profile,
    }
    
    return render(request, 'UserInfomation.html', context)

@login_required
def refresh_user_cache(request):
    """刷新当前用户缓存（手动清除）"""
    if request.method == 'POST':
        clear_user_cache_by_username(request.user.name)
        return JsonResponse({'success': True, 'message': '缓存已刷新'})
    return JsonResponse({'error': '无效请求'}, status=400)

def user_search_api(request):
    """用户搜索API"""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'users': []})
    
    users = search_users_by_name(query, limit=10)
    return JsonResponse({'users': users})