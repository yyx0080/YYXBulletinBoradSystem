from django.conf import settings
from django.db import models

from Userlogin.models import UserInfo


# Create your models here.
#留言表模型
class BoardInfo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(
        max_length=20, 
        db_index=True,
        help_text="留言用户名（兼容历史数据）"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='boards',
        help_text="关联用户（新增功能）"
    )
    content = models.TextField(verbose_name="留言内容")  # 使用 TextField 存储富文本内容
    board_date = models.DateTimeField(db_index=True)  # 改为 DateTimeField 支持精确到秒，添加索引
    like_point = models.IntegerField(default=0)
    image_path = models.CharField(max_length=255, blank=True, default='')
    type = models.IntegerField()
    dontlike_point = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            # models.Index(fields=['board_date', 'type']),
            models.Index(fields=['username', 'board_date']),
            # 时间排序索引
            models.Index(fields=['-board_date']),
            models.Index(fields=['board_date']),
            
            # 点赞排序索引
            models.Index(fields=['-like_point', '-board_date']),
            models.Index(fields=['like_point', '-board_date']),
        ]
        ordering = ['-board_date']
    
    def save(self, *args, **kwargs):
        # 自动同步username和user关系
        if self.user and not self.username:
            self.username = self.user.name
        elif not self.user and self.username:
            try:
                self.user = UserInfo.objects.get(name=self.username)
            except UserInfo.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    @property
    def display_username(self):
        """智能显示用户名"""
        if self.user and self.user.is_active:
            return self.user.name
        return self.username

    # @property
    # def user_avatar(self):
    #     """获取用户头像（未来扩展）"""
    #     if self.user and hasattr(self.user, 'avatar'):
    #         return self.user.avatar
    #     return None