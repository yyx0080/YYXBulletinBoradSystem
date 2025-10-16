from django.core.management.base import BaseCommand
from BoardManagement.models import BoardInfo
from Userlogin.models import UserInfo

class Command(BaseCommand):
    help = '迁移BoardInfo的username到user外键'

    def handle(self, *args, **options):
        migrated = 0
        for board in BoardInfo.objects.filter(user__isnull=True):
            try:
                user = UserInfo.objects.get(name=board.username)
                board.user = user
                board.save()
                migrated += 1
                if migrated % 100 == 0:
                    self.stdout.write(f'已迁移 {migrated} 条记录...')
            except UserInfo.DoesNotExist:
                # 保持原样，username字段确保数据可见
                continue
        
        self.stdout.write(
            self.style.SUCCESS(f'成功迁移 {migrated} 条记录')
        )