# 写处理数据库的操作（中间件）
import requests
import json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import Conversation, Message
from Userlogin.models import UserInfo

# 根据当前用户、指定对话以及问题，获取DeepSeek答复，并将问答内容存入数据库，返回答复内容
def get_deepseek_response(user, conversation_id, prompt):
    try:
        # 获取当前用户和对话
        conversation = Conversation.objects.get(id=conversation_id, user=user)
        
        # 构建历史消息
        message_history = list(conversation.messages.all().order_by('created_at').values('role', 'content'))
        message_history.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": message_history,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(
            settings.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30  # 设置超时时间
        )
        response.raise_for_status()
        
        # 解析响应
        response_data = response.json()
        assistant_reply = response_data['choices'][0]['message']['content']
        tokens_used = response_data['usage']['total_tokens']
        
        # 保存用户消息
        user_message = Message.objects.create(
            conversation=conversation,
            role='user',
            content=prompt,
            tokens=response_data['usage']['prompt_tokens']
        )
        
        # 保存助手回复
        assistant_message = Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=assistant_reply,
            tokens=response_data['usage']['completion_tokens']
        )
        
        # 更新对话标题（如果是第一条消息）
        if conversation.messages.count() == 2:  # 用户+助手
            conversation.title = generate_title(prompt)
        
        # 更新token使用
        conversation.token_used += tokens_used
        conversation.save()
        
        # 更新用户积分（如果需要）
        # if hasattr(settings, 'POINT_PER_TOKEN') and settings.POINT_PER_TOKEN > 0:
        #     points_to_deduct = tokens_used * settings.POINT_PER_TOKEN
        #     if user.point >= points_to_deduct:
        #         user.point -= points_to_deduct
        #         user.save()
        #     else:
        #         return "积分不足，请充值后再使用", 0
        
        return assistant_reply, tokens_used
        
    except ObjectDoesNotExist:
        return "对话不存在或您没有访问权限", 0
    except requests.exceptions.RequestException as e:
        return f"API请求错误: {str(e)}", 0
    except Exception as e:
        return f"系统错误: {str(e)}", 0

def generate_title(prompt):
    """使用第一条消息生成对话标题"""
    if len(prompt) > 40:
        return prompt[:40] + "..."
    return prompt
