from django.db.models import F
from BoardManagement.models import BoardInfo
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg, Max, Min
#这里用来写数据库的操作

def GetBoardInfo(sort_type='newest', use_user_relation=False):
    """
    获取留言板信息，支持多种排序方式
    
    Args:
        sort_type: 排序类型 ('newest', 'oldest', 'most_likes', 'least_likes')
        use_user_relation: 是否使用关联查询
    """
    # 基础查询集
    if use_user_relation:
        queryset = BoardInfo.objects.select_related('user')
    else:
        queryset = BoardInfo.objects.all()
    
    # 应用排序
    sort_mapping = {
        'newest': '-board_date',
        'oldest': 'board_date',
        'most_likes': '-like_point',
        'least_likes': 'like_point',
    }
    
    order_field = sort_mapping.get(sort_type, '-board_date')
    
    # 添加二级排序确保稳定性，点赞数一致时按时间排序
    if sort_type in ['most_likes', 'least_likes']:
        queryset = queryset.order_by(order_field, '-board_date')
    else:
        queryset = queryset.order_by(order_field)
    
    return queryset

def GetBoardInfoPaginated(sort_type='newest', use_user_relation=False, page=1, page_size=10):
    """
    获取分页的留言板信息
    
    Args:
        sort_type: 排序类型
        use_user_relation: 是否使用关联查询
        page: 页码
        page_size: 每页数量
    """
    
    queryset = GetBoardInfo(sort_type, use_user_relation)
    paginator = Paginator(queryset, page_size)
    
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return page_obj

def GetBoardStats():
    """获取留言板统计信息"""
    
    stats = BoardInfo.objects.aggregate(
        total_count=Count('id'),
        avg_likes=Avg('like_point'),
        max_likes=Max('like_point'),
        min_likes=Min('like_point'),
        latest_post=Max('board_date'),
    )
    
    return stats
# # 取出所有留言，展示给前端
# def GetBoardInfo(use_user_relation=False):
#     if use_user_relation:
#         # 需要用户详情时使用关联查询
#         return BoardInfo.objects.select_related('user').order_by('-board_date')
#     else:
#         # 普通列表使用，性能更优
#         return BoardInfo.objects.all().order_by('-board_date')

# 测试函数，用来添加一些测试数据进去
#测试接口
def TestAddBoardInfo():
    current_time = datetime.now()  # 获取当前时间，类型为datetime.datetime
    print(current_time)
    
    # 插入测试数据
    BoardInfo.objects.create(username="test01", content="这是 test01 的留言内容。", board_date=current_time, like_point=10, image_path='', type=1)
    BoardInfo.objects.create(username="test02", content="这是 test02 的特别留言。", board_date=current_time, like_point=5, image_path='', type=1)
    BoardInfo.objects.create(username="test03", content="test03 留了一条有趣的评论。", board_date=current_time, like_point=15, image_path='/path/to/image.jpg', type=2)
    BoardInfo.objects.create(username="yyx", content="yyx 的留言有一些特殊字符 #$%@!", board_date=current_time, like_point=20, image_path='', type=1)

#将用户评论添加到数据库中
def AddUserComment(user, content):
    # 创建留言并保存到数据库
    current_time = datetime.now()  # 获取当前时间，秒级
    print(current_time)
    BoardInfo.objects.create(
        username=user.name,  # 使用登录用户的用户名，保持兼容
        user = user,
        content=content, 
        board_date=current_time, 
        like_point=0,
        image_path='',
        type=0  # 留言类型为普通留言
    )