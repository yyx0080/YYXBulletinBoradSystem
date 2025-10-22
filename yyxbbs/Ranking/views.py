from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .ormoperator import (
    get_like_ranking, get_point_ranking, get_combined_ranking, 
    get_user_rank, create_ranking_snapshot
)
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@login_required
def ranking_board(request):
    """排行榜主页面"""
    like_ranking = get_like_ranking(20)
    point_ranking = get_point_ranking(20)
    combined_ranking = get_combined_ranking(20)
    
    # 获取当前用户排名
    current_user_rank = {}
    if request.user.is_authenticated:
        current_user_rank = {
            'like_rank': get_user_rank(request.user, 'like'),
            'point_rank': get_user_rank(request.user, 'point'),
            'combined_rank': get_user_rank(request.user, 'combined'),
            'user_data': {
                'name': request.user.name,
                'total_likes': request.user.total_likes,
                'point': request.user.point,
                'combined_score': request.user.total_likes + request.user.point
            }
        }
    
    context = {
        'like_ranking': like_ranking,
        'point_ranking': point_ranking,
        'combined_ranking': combined_ranking,
        'current_user_rank': current_user_rank,
    }
    return render(request, 'ranking.html', context)

@require_http_methods(["GET"])
def ranking_api(request, ranking_type):
    """排行榜API接口"""
    limit = int(request.GET.get('limit', 20))
    
    if ranking_type == 'like':
        data = get_like_ranking(limit)
    elif ranking_type == 'point':
        data = get_point_ranking(limit)
    elif ranking_type == 'combined':
        data = get_combined_ranking(limit)
    else:
        return JsonResponse({'error': '无效的排行榜类型'}, status=400)
    
    ranking_list = []
    for index, user in enumerate(data, 1):
        ranking_list.append({
            'rank': index,
            'name': user.name,
            'total_likes': user.total_likes,
            'point': user.point,
            'combined_score': user.total_likes + user.point
        })
    
    return JsonResponse({'ranking': ranking_list})

@login_required
@require_http_methods(["GET"])
def my_ranking_api(request):
    """获取当前用户排名API"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': '未登录'}, status=401)
    
    user_rank = {
        'like_rank': get_user_rank(request.user, 'like'),
        'point_rank': get_user_rank(request.user, 'point'),
        'combined_rank': get_user_rank(request.user, 'combined'),
        'user_data': {
            'name': request.user.name,
            'total_likes': request.user.total_likes,
            'point': request.user.point,
            'combined_score': request.user.total_likes + request.user.point
        }
    }
    
    return JsonResponse(user_rank)