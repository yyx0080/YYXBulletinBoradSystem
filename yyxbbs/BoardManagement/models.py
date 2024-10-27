from django.db import models

# Create your models here.
#留言表模型
class BoradInfo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    content = models.TextField()  # 使用 TextField 存储富文本内容
    board_date = models.DateTimeField()  # 改为 DateTimeField 支持精确到秒
    like_point = models.IntegerField(default=0)
    image_path = models.CharField(max_length=100, blank=True, default='')
    type = models.IntegerField()
    dontlike_point = models.IntegerField(default=0)