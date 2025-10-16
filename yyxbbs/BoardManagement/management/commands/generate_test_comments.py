import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.apps import apps
from datetime import timedelta

class Command(BaseCommand):
    help = '生成10000条测试评论数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10000,
            help='要生成的评论数量（默认10000）'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='每批处理的数量（默认1000）'
        )

    def handle(self, *args, **options):
        # 获取模型
        BoardInfo = apps.get_model('BoardManagement', 'BoardInfo')
        UserInfo = apps.get_model('Userlogin', 'UserInfo')
        
        count = options['count']
        batch_size = options['batch_size']
        
        # 获取所有用户
        users = list(UserInfo.objects.all())
        if not users:
            self.stderr.write(self.style.ERROR('没有找到任何用户，请先创建用户'))
            return
        
        self.stdout.write(f'找到 {len(users)} 个用户')
        self.stdout.write(f'开始生成 {count} 条测试评论...')
        
        # 评论内容模板
        comments_content = [
            "今天天气真不错！",
            "这个网站太棒了！",
            "感谢分享，学到了很多",
            "期待后续更新",
            "有没有人一起讨论？",
            "测试评论内容",
            "这个设计很巧妙",
            "支持一下！",
            "mark一下，以后来看",
            "不错的观点，我赞同",
            "有人遇到过同样的问题吗？",
            "求大神解答",
            "收藏了，慢慢看",
            "顶一下好网站",
            "路过留个言",
            "持续关注中",
            "感谢分享",
            "这个思路很新颖",
            "实践了一下，确实有效",
            "希望越来越好"
        ]
        
        # 批量创建评论
        boards_to_create = []
        start_time = timezone.now() - timedelta(days=365)  # 一年前开始
        
        for i in range(count):
            # 随机选择用户
            user = random.choice(users)
            
            # 随机时间（从一年前到现在）
            random_days = random.randint(0, 365)
            random_hours = random.randint(0, 23)
            random_minutes = random.randint(0, 59)
            board_date = start_time + timedelta(
                days=random_days, 
                hours=random_hours, 
                minutes=random_minutes
            )
            
            # 随机内容
            content = random.choice(comments_content)
            if random.random() < 0.3:  # 30%的概率添加额外内容
                content += " " + " ".join([random.choice(comments_content) for _ in range(random.randint(1, 3))])
            
            # 随机点赞数
            like_point = random.randint(0, 1000)
            
            # 创建BoardInfo对象
            board = BoardInfo(
                username=user.name,
                user=user,
                content=content,
                board_date=board_date,
                like_point=like_point,
                dontlike_point=0,
                image_path='',
                type=0
            )
            boards_to_create.append(board)
            
            # 批量提交
            if len(boards_to_create) >= batch_size:
                BoardInfo.objects.bulk_create(boards_to_create)
                self.stdout.write(f'已创建 {i+1}/{count} 条评论')
                boards_to_create = []
        
        # 提交剩余记录
        if boards_to_create:
            BoardInfo.objects.bulk_create(boards_to_create)
        
        self.stdout.write(
            self.style.SUCCESS(f'成功生成 {count} 条测试评论！')
        )