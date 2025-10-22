from django.db import models
from Userlogin.models import UserInfo
from BoardManagement.models import BoardInfo
from Ranking.ormoperator import get_user_rank
from django.core.paginator import Paginator
from django.core.cache import cache



# 根据用户名取得用户信息
def GetUserInfoByUsername(username):
    userinfo = UserInfo.objects.get(name=username)
    return userinfo

def get_user_profile_by_username(username):
    """通过用户名获取用户基本信息"""
    cache_key = f'user_profile_{username}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    try:
        user = UserInfo.objects.get(name=username, is_active=True)
        profile_data = {
            'id': user.id,
            'name': user.name,
            'point': user.point,
            'total_likes': user.total_likes,
            'last_attendance_date': user.last_attendance_date,
            'login_date': user.login_date,
            'last_login_date': user.last_login_date,
        }
        
        # 缓存10分钟
        cache.set(cache_key, profile_data, 600)
        return profile_data
    except UserInfo.DoesNotExist:
        return None

def get_user_profile_by_id(user_id):
    """通过用户ID获取用户基本信息（内部使用）"""
    try:
        user = UserInfo.objects.get(id=user_id, is_active=True)
        return {
            'id': user.id,
            'name': user.name,
            'point': user.point,
            'total_likes': user.total_likes,
            'last_attendance_date': user.last_attendance_date,
            'login_date': user.login_date,
            'last_login_date': user.last_login_date,
        }
    except UserInfo.DoesNotExist:
        return None

def get_user_comments_by_username(username, page=1, page_size=10):
    """通过用户名获取用户的留言列表（分页）"""
    cache_key = f'user_comments_{username}_page{page}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    try:
        user = UserInfo.objects.get(name=username, is_active=True)
        comments = BoardInfo.objects.filter(
            user=user
        ).select_related('user').order_by('-board_date')
        
        paginator = Paginator(comments, page_size)
        try:
            page_obj = paginator.page(page)
        except:
            page_obj = paginator.page(1)
        
        result = {
            'comments': list(page_obj.object_list.values(
                'id', 'content', 'board_date', 'like_point'
            )),
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_comments': paginator.count,
        }
        
        # 缓存5分钟
        cache.set(cache_key, result, 300)
        return result
    except UserInfo.DoesNotExist:
        return None

def get_user_stats_by_username(username):
    """通过用户名获取用户统计数据"""
    cache_key = f'user_stats_{username}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    try:
        user = UserInfo.objects.get(name=username, is_active=True)
        comments = BoardInfo.objects.filter(user=user)
        total_comments = comments.count()
        
        stats = {
            'total_comments': total_comments,
            'total_likes_received': comments.aggregate(
                total_likes=models.Sum('like_point')
            )['total_likes'] or 0,
            'avg_likes_per_comment': comments.aggregate(
                avg_likes=models.Avg('like_point')
            )['avg_likes'] or 0,
        }
        
        # 缓存10分钟
        cache.set(cache_key, stats, 600)
        return stats
    except UserInfo.DoesNotExist:
        return None

def get_user_ranks_by_username(username):
    """通过用户名获取用户排名信息"""
    cache_key = f'user_ranks_{username}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    try:
        user = UserInfo.objects.get(name=username, is_active=True)
        ranks = {
            'like_rank': get_user_rank(user, 'like'),
            'point_rank': get_user_rank(user, 'point'),
            'combined_rank': get_user_rank(user, 'combined'),
        }
        
        # 缓存5分钟（排名变化相对频繁）
        cache.set(cache_key, ranks, 300)
        return ranks
    except UserInfo.DoesNotExist:
        return None

def clear_user_cache_by_username(username):
    """通过用户名清除用户相关缓存"""
    cache_patterns = [
        f'user_profile_{username}',
        f'user_comments_{username}_*',
        f'user_stats_{username}',
        f'user_ranks_{username}',
    ]
    
    for pattern in cache_patterns:
        keys = cache.keys(pattern)
        if keys:
            cache.delete_many(keys)

def clear_user_cache_by_id(user_id):
    """通过用户ID清除用户相关缓存（内部使用）"""
    try:
        user = UserInfo.objects.get(id=user_id, is_active=True)
        clear_user_cache_by_username(user.name)
    except UserInfo.DoesNotExist:
        pass

def search_users_by_name(username_query, limit=10):
    """根据用户名搜索用户"""
    cache_key = f'user_search_{username_query}_{limit}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    users = UserInfo.objects.filter(
        name__icontains=username_query,
        is_active=True
    ).values('id', 'name', 'point', 'total_likes')[:limit]
    
    # 缓存2分钟
    cache.set(cache_key, list(users), 120)
    return list(users)