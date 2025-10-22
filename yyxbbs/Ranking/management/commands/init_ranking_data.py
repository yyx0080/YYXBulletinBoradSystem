from django.core.management.base import BaseCommand
from Userlogin.models import UserInfo
from BoardManagement.models import BoardInfo
from django.db.models import Sum
from Ranking.ormoperator import update_user_total_likes

class Command(BaseCommand):
    help = '初始化用户总点赞量数据'

    def handle(self, *args, **options):
        users = UserInfo.objects.all()
        total_users = users.count()
        
        self.stdout.write(f'开始初始化 {total_users} 个用户的总点赞量...')
        
        for index, user in enumerate(users, 1):
            # 计算用户总点赞量
            total_likes = BoardInfo.objects.filter(user=user).aggregate(
                total=Sum('like_point')
            )['total'] or 0
            
            user.total_likes = total_likes
            user.save()
            
            if index % 10 == 0:
                self.stdout.write(f'已处理 {index}/{total_users} 个用户...')
        
        self.stdout.write(
            self.style.SUCCESS('成功初始化所有用户的总点赞量！')
        )