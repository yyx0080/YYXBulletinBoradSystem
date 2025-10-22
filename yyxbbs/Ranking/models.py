from django.db import models
from django.conf import settings

# Create your models here.

class RankingSnapshot(models.Model):
    """排行榜快照，用于缓存和记录历史排名"""
    RANKING_TYPES = [
        ('like', '点赞榜'),
        ('point', '积分榜'),
        ('combined', '综合榜'),
    ]
    
    ranking_type = models.CharField(max_length=10, choices=RANKING_TYPES)
    snapshot_data = models.JSONField()  # 存储排名数据
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['ranking_type', '-created_at']),  # 按类型和时间查询
            models.Index(fields=['-created_at']),  # 时间排序
        ]
        ordering = ['-created_at']
        verbose_name = '排行榜快照'
        verbose_name_plural = '排行榜快照'
    
    def __str__(self):
        return f"{self.get_ranking_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"