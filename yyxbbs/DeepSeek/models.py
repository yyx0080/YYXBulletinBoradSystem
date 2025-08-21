from django.db import models
from django.conf import settings
from Userlogin.models import UserInfo

# Create your models here.

#DeepSeek表模型
class Conversation(models.Model):
    """存储对话会话的元数据"""
    user = models.ForeignKey(
        UserInfo, 
        on_delete=models.CASCADE,
        related_name='conversations',
        verbose_name='用户'
    )
    title = models.CharField(max_length=200, verbose_name='标题')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    token_used = models.IntegerField(default=0, verbose_name='Token消耗')  # 本次对话总token消耗

    class Meta:
        verbose_name = '对话'
        verbose_name_plural = '对话记录'
        ordering = ['-updated_at']  # 默认按更新时间倒序排列

    def __str__(self):
        return f"{self.user.name} - {self.title}"

class Message(models.Model):
    """存储单条对话消息"""
    ROLE_CHOICES = [
        ('user', '用户'),
        ('assistant', '助手'),
    ]
    
    conversation = models.ForeignKey(
        Conversation, 
        related_name='messages', 
        on_delete=models.CASCADE,
        verbose_name='所属对话'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='角色')
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    tokens = models.IntegerField(default=0, verbose_name='Token数')

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息记录'
        ordering = ['created_at']  # 按创建时间正序排列

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"