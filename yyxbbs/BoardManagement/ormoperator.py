from django.db.models import F
from BoardManagement.models import BoardInfo
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Avg, Max, Min, Q
import json
import base64
from urllib.parse import quote, unquote
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

def GetBoardInfoPaginated(sort_type='newest', use_user_relation=False, use_cursor=False, cursors=None, page=1, page_size=10, direction='next'):
    """
    获取分页的留言板信息
    
    Args:
        sort_type: 排序类型
        use_user_relation: 是否使用关联查询
        use_cursor: 是否使用游标排序
        cursors: 上一页最后一条记录的值字典，对应游标
        page: 页码
        page_size: 每页数量
        direction: 分页方向 'next' 或 'prev'
    """
    
    queryset = GetBoardInfo(sort_type, use_user_relation)
    if use_cursor == False:
        paginator = Paginator(queryset, page_size)
        
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        return page_obj
    else:
        if sort_type == 'newest':
            if cursors:
                # cursors = {'board_date': '2024-01-01 10:00:00'}
                if direction == 'next':
                    # 下一页：取比当前页最后一条记录更早的记录
                    queryset = queryset.filter(board_date__lt=cursors['board_date'])
                else:
                    # 上一页：取比当前页第一条记录更晚的记录
                    queryset = queryset.filter(board_date__gt=cursors['board_date'])
                    # 上一页需要反转顺序，因为要的是比当前第一条记录更新的记录
                    queryset = queryset.order_by('board_date')
                
        elif sort_type == 'oldest':
            if cursors:
                if direction == 'next':
                    # 下一页：取比当前页最后一条记录更晚的记录
                    queryset = queryset.filter(board_date__gt=cursors['board_date'])
                else:
                    # 上一页：取比当前页第一条记录更早的记录
                    queryset = queryset.filter(board_date__lt=cursors['board_date'])
                    queryset = queryset.order_by('-board_date')
                
        elif sort_type == 'most_likes':
            if cursors:
                if direction == 'next':
                    # 下一页：取比当前页最后一条记录点赞更少或相同点赞但更早的记录
                    queryset = queryset.filter(
                        Q(like_point__lt=cursors['like_point']) |
                        Q(like_point=cursors['like_point'], 
                            board_date__lt=cursors['board_date'])
                    )
                else:
                    # 上一页：取比当前页第一条记录点赞更多或相同点赞但更晚的记录
                    queryset = queryset.filter(
                        Q(like_point__gt=cursors['like_point']) |
                        Q(like_point=cursors['like_point'], 
                            board_date__gt=cursors['board_date'])
                    )
                    queryset = queryset.order_by('like_point', 'board_date')
                
        elif sort_type == 'least_likes':
            if cursors:
                if direction == 'next':
                    # 下一页：取比当前页最后一条记录点赞更多或相同点赞但更晚的记录
                    queryset = queryset.filter(
                        Q(like_point__gt=cursors['like_point']) |
                        Q(like_point=cursors['like_point'], 
                            board_date__gt=cursors['board_date'])
                    )
                else:
                    # 上一页：取比当前页第一条记录点赞更少或相同点赞但更早的记录
                    queryset = queryset.filter(
                        Q(like_point__lt=cursors['like_point']) |
                        Q(like_point=cursors['like_point'], 
                            board_date__lt=cursors['board_date'])
                    )
                    queryset = queryset.order_by('-like_point', '-board_date')

        # 对于上一页，我们需要反转结果顺序（因为得到的数据是按照相反的排序方式得到的）
        if direction == 'prev':
            results = list(queryset[:page_size + 1])
            # 反转结果，使其保持正确的排序顺序
            results.reverse()
            return results
        else:
            return list(queryset[:page_size + 1])

def has_previous_page(sort_type, first_comment):
    """
    判断是否有上一页
    """
    queryset = BoardInfo.objects.all()
    
    if sort_type == 'newest':
        # 是否有比当前页第一条记录更新的记录
        return queryset.filter(board_date__gt=first_comment.board_date).exists()
    elif sort_type == 'oldest':
        # 是否有比当前页第一条记录更旧的记录
        return queryset.filter(board_date__lt=first_comment.board_date).exists()
    elif sort_type == 'most_likes':
        # 是否有比当前页第一条记录点赞更多或相同点赞但更新的记录
        return queryset.filter(
            Q(like_point__gt=first_comment.like_point) |
            Q(like_point=first_comment.like_point, 
             board_date__gt=first_comment.board_date)
        ).exists()
    elif sort_type == 'least_likes':
        # 是否有比当前页第一条记录点赞更少或相同点赞但更旧的记录
        return queryset.filter(
            Q(like_point__lt=first_comment.like_point) |
            Q(like_point=first_comment.like_point, 
             board_date__lt=first_comment.board_date)
        ).exists()
    
    return False

def create_keyset_cursor(instance, sort_type):
    """
    创建键集游标
    返回一个包含排序字段值的字典
    """
    cursor_data = {}
    
    if sort_type in ['newest', 'oldest']:
        cursor_data['board_date'] = instance.board_date.isoformat()
    elif sort_type in ['most_likes', 'least_likes']:
        cursor_data['like_point'] = instance.like_point
        cursor_data['board_date'] = instance.board_date.isoformat()
    
    return cursor_data

def serialize_cursor(cursor_data):
    """
    安全序列化游标 - 使用JSON + Base64编码
    """
    if not cursor_data:
        return None
    
    try:
        # 将字典转换为JSON字符串
        json_str = json.dumps(cursor_data)
        # Base64编码，避免URL特殊字符问题
        encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        # URL编码，确保安全传输
        return quote(encoded)
    except Exception as e:
        print(f"游标序列化错误: {e}")
        return None

def deserialize_cursor(cursor_str):
    """
    安全反序列化游标
    """
    if not cursor_str:
        return None
    
    try:
        # URL解码
        decoded = unquote(cursor_str)
        # Base64解码
        json_str = base64.b64decode(decoded).decode('utf-8')
        # JSON解析
        return json.loads(json_str)
    except Exception as e:
        print(f"游标反序列化错误: {e}, 游标字符串: {cursor_str}")
        return None

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