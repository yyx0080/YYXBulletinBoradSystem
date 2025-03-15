from BoardManagement.models import BoradInfo
from datetime import datetime
#这里用来写数据库的操作


# 取出所有留言，展示给前端
def GetBoradInfo():
    borad_info_list = BoradInfo.objects.all().order_by('-board_date')  # 按日期降序排列
    return borad_info_list

# 测试函数，用来添加一些测试数据进去
#测试接口
def TestAddBoradInfo():
    current_time = datetime.now()  # 获取当前时间，类型为datetime.datetime
    print(current_time)
    
    # 插入测试数据
    BoradInfo.objects.create(username="test01", content="这是 test01 的留言内容。", board_date=current_time, like_point=10, image_path='', type=1)
    BoradInfo.objects.create(username="test02", content="这是 test02 的特别留言。", board_date=current_time, like_point=5, image_path='', type=1)
    BoradInfo.objects.create(username="test03", content="test03 留了一条有趣的评论。", board_date=current_time, like_point=15, image_path='/path/to/image.jpg', type=2)
    BoradInfo.objects.create(username="yyx", content="yyx 的留言有一些特殊字符 #$%@!", board_date=current_time, like_point=20, image_path='', type=1)

#将用户评论添加到数据库中
def AddUserComment(username, content):
    # 创建留言并保存到数据库
    current_time = datetime.now()  # 获取当前时间，秒级
    print(current_time)
    BoradInfo.objects.create(
        username=username,  # 使用登录用户的用户名
        content=content, 
        board_date=current_time, 
        like_point=0,
        image_path='',
        type=0  # 留言类型为普通留言
    )

def AddLikePointByCommentId(commentid):
    comment = BoradInfo.objects.get(id=commentid)
    if comment:
        comment.like_point += 1
        comment.save()
        return True
    else:
        return False

def GetLikePointByCommentId(commentid):
    return BoradInfo.objects.get(id=commentid).like_point