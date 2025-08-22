# 写处理数据库的操作（中间件）
from .models import Conversation, Message
from Userlogin.models import UserInfo
from django.utils import timezone

# 获取用户的对话列表
def get_user_conversations(user):
    return Conversation.objects.filter(user=user).order_by('-updated_at')

# 获取特定对话的消息
def get_conversation_messages(conversation_id, user):
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=user)
        return conversation.messages.all().order_by('created_at')
    except Conversation.DoesNotExist:
        return None

# 创建新对话
def create_conversation(user, title="新对话"):
    return Conversation.objects.create(user=user, title=title)

# 添加消息到对话
def add_message_to_conversation(conversation, role, content, tokens=0):
    message = Message.objects.create(
        conversation=conversation,
        role=role,
        content=content,
        tokens=tokens
    )
    
    # 更新对话的 Token 使用量和更新时间
    conversation.token_used += tokens
    conversation.updated_at = timezone.now()
    conversation.save()
    
    return message

# 删除对话
def delete_conversation(conversation_id, user):
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=user)
        conversation.delete()
        return True
    except Conversation.DoesNotExist:
        return False

# 更新对话标题
def update_conversation_title(conversation_id, user, title):
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=user)
        conversation.title = title
        conversation.save()
        return True
    except Conversation.DoesNotExist:
        return False