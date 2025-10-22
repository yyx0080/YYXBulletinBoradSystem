from Userlogin.models import UserInfo
from BoardManagement.models import BoardInfo
from django.db.models import F, Sum
from .models import RankingSnapshot
from django.core.cache import cache
import json

def update_user_total_likes(user):
    """更新用户总点赞量"""
    total = BoardInfo.objects.filter(user=user).aggregate(
        total_likes=Sum('like_point')
    )['total_likes'] or 0
    
    user.total_likes = total
    user.save()
    # 清除排行榜缓存
    clear_ranking_cache()

def get_like_ranking(limit=20):
    """获取点赞量排名（带缓存）"""
    cache_key = f'like_ranking_{limit}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    ranking = UserInfo.objects.filter(
        is_active=True,
        total_likes__gt=0  # 只显示有点赞的用户
    ).order_by('-total_likes', '-point')[:limit]
    
    # 缓存1小时
    cache.set(cache_key, ranking, 3600)
    return ranking

def get_point_ranking(limit=20):
    """获取积分排名（带缓存）"""
    cache_key = f'point_ranking_{limit}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    ranking = UserInfo.objects.filter(
        is_active=True,
        point__gt=0  # 只显示有积分的用户
    ).order_by('-point', '-total_likes')[:limit]
    
    cache.set(cache_key, ranking, 3600)
    return ranking

def get_combined_ranking(limit=20):
    """获取综合排名（点赞量+积分）"""
    cache_key = f'combined_ranking_{limit}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    ranking = UserInfo.objects.filter(
        is_active=True
    ).annotate(
        combined_score=F('total_likes') + F('point')
    ).filter(
        combined_score__gt=0
    ).order_by('-combined_score', '-total_likes')[:limit]
    
    cache.set(cache_key, ranking, 3600)
    return ranking

def get_user_rank(user, ranking_type='combined'):
    """获取用户在特定排行榜中的排名"""
    if ranking_type == 'like':
        # 计算点赞排名
        higher_users = UserInfo.objects.filter(
            is_active=True,
            total_likes__gt=user.total_likes
        ).count()
        return higher_users + 1
        
    elif ranking_type == 'point':
        # 计算积分排名
        higher_users = UserInfo.objects.filter(
            is_active=True,
            point__gt=user.point
        ).count()
        return higher_users + 1
        
    else:  # combined
        # 计算综合排名
        higher_users = UserInfo.objects.filter(
            is_active=True
        ).annotate(
            combined_score=F('total_likes') + F('point')
        ).filter(
            combined_score__gt=(user.total_likes + user.point)
        ).count()
        return higher_users + 1

def clear_ranking_cache():
    """清除排行榜缓存"""
    cache_keys = ['like_ranking_', 'point_ranking_', 'combined_ranking_']
    for key in cache_keys:
        cache.delete_pattern(f'{key}*')

def create_ranking_snapshot():
    """创建排行榜快照"""
    like_ranking = list(get_like_ranking(50).values('id', 'name', 'total_likes'))
    point_ranking = list(get_point_ranking(50).values('id', 'name', 'point'))
    combined_ranking = list(get_combined_ranking(50).values('id', 'name', 'total_likes', 'point'))
    
    # 存储点赞榜快照
    RankingSnapshot.objects.create(
        ranking_type='like',
        snapshot_data=like_ranking
    )
    
    # 存储积分榜快照
    RankingSnapshot.objects.create(
        ranking_type='point',
        snapshot_data=point_ranking
    )
    
    # 存储综合榜快照
    RankingSnapshot.objects.create(
        ranking_type='combined',
        snapshot_data=combined_ranking
    )