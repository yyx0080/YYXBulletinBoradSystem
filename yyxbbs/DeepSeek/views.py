import json
import requests
import tiktoken  # 用于计算 Token 数量
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.cache import cache
from .models import Conversation, Message
from .ormoperator import (
    get_user_conversations, get_conversation_messages,
    create_conversation, add_message_to_conversation,
    delete_conversation, update_conversation_title
)

# @login_required保证这个接口只能由登录的用户来调用
# Create your views here.
# 在该文件中写功能函数，在urls.py中写上对应关系，在对应html文件中调用urls.py中的新命名

# 初始化 Tokenizer
try:
    tokenizer = tiktoken.get_encoding("cl100k_base")
except:
    tokenizer = None

def count_tokens(text):
    """计算文本的 Token 数量"""
    if tokenizer and text:
        return len(tokenizer.encode(text))
    return 0

def call_deepseek_api(messages, max_tokens=2000):
    """调用 DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "stream": False
    }
    
    try:
        response = requests.post(
            settings.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30  # 30秒超时
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"DeepSeek API 调用失败: {e}")
        return None

def rate_limit_check(user, limit=10, period=60):
    """检查速率限制"""
    key = f"deepseek_rate_limit_{user.id}"
    count = cache.get(key, 0)
    
    if count >= limit:
        return False
    
    cache.set(key, count + 1, period)
    return True

def clean_input(text):
    """清理用户输入"""
    import html
    # 基本的HTML转义防止XSS
    cleaned = html.escape(text)
    # 移除过长的输入
    if len(cleaned) > 1000:
        cleaned = cleaned[:1000]
    return cleaned

# 开始新对话
@csrf_exempt
@require_http_methods(["POST"])
def start_conversation(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "未登录"}, status=401)
    
    # 创建新对话
    conversation = create_conversation(request.user)
    
    # 创建欢迎消息
    welcome_message = "您好！我是DeepSeek AI助手，很高兴为您服务。请问有什么我可以帮助您的吗？"
    welcome_tokens = count_tokens(welcome_message)
    add_message_to_conversation(conversation, "assistant", welcome_message, welcome_tokens)
    
    return JsonResponse({
        "conversation_id": conversation.id,
        "title": conversation.title
    })

# 聊天API
@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "未登录"}, status=401)
    
    # 检查速率限制
    if not rate_limit_check(request.user):
        return JsonResponse({"error": "请求过于频繁，请稍后再试"}, status=429)
    
    conversation_id = request.POST.get("conversation_id")
    prompt = clean_input(request.POST.get("prompt", "").strip())
    
    if not prompt:
        return JsonResponse({"error": "消息内容不能为空"}, status=400)
    
    # 获取对话
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
    except Conversation.DoesNotExist:
        return JsonResponse({"error": "对话不存在或无权访问"}, status=404)
    
    # 保存用户消息
    user_tokens = count_tokens(prompt)
    add_message_to_conversation(conversation, "user", prompt, user_tokens)
    
    # 构建对话历史
    messages = []
    for msg in conversation.messages.all().order_by('created_at'):
        messages.append({"role": msg.role, "content": msg.content})
    
    # 调用DeepSeek API
    api_response = call_deepseek_api(messages)
    
    if not api_response:
        error_msg = "AI服务暂时不可用，请稍后再试"
        error_tokens = count_tokens(error_msg)
        add_message_to_conversation(conversation, "assistant", error_msg, error_tokens)
        return JsonResponse({"error": error_msg}, status=503)
    
    # 提取AI回复和Token使用情况
    choices = api_response.get("choices", [{}])
    if not choices:
        error_msg = "AI返回格式错误"
        error_tokens = count_tokens(error_msg)
        add_message_to_conversation(conversation, "assistant", error_msg, error_tokens)
        return JsonResponse({"error": error_msg}, status=500)
    
    ai_response = choices[0].get("message", {}).get("content", "抱歉，我无法回答这个问题。")
    
    # 计算AI回复的Token数量
    usage = api_response.get("usage", {})
    ai_tokens = usage.get("completion_tokens", count_tokens(ai_response))
    
    # 保存AI回复
    add_message_to_conversation(conversation, "assistant", ai_response, ai_tokens)
    
    # 更新对话标题（如果是第一条用户消息）
    if conversation.messages.filter(role="user").count() == 1:
        title = prompt[:30] + "..." if len(prompt) > 30 else prompt
        update_conversation_title(conversation.id, request.user, title)
    
    return JsonResponse({
        "response": ai_response,
        "tokens": ai_tokens,
        "total_tokens": conversation.token_used
    })

# 获取对话列表
@require_http_methods(["GET"])
def conversation_list_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "未登录"}, status=401)
    
    conversations = get_user_conversations(request.user)
    
    conversation_list = []
    for conv in conversations:
        conversation_list.append({
            "id": conv.id,
            "title": conv.title,
            "updated_at": conv.updated_at.isoformat(),
            "token_used": conv.token_used
        })
    
    return JsonResponse(conversation_list, safe=False)

# 获取对话消息
@require_http_methods(["GET"])
def conversation_messages_api(request, conversation_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "未登录"}, status=401)
    
    messages = get_conversation_messages(conversation_id, request.user)
    if messages is None:
        return JsonResponse({"error": "对话不存在或无权访问"}, status=404)
    
    message_list = []
    for msg in messages:
        message_list.append({
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat(),
            "tokens": msg.tokens
        })
    
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        return JsonResponse({
            "id": conversation.id,
            "title": conversation.title,
            "token_used": conversation.token_used,
            "messages": message_list
        })
    except Conversation.DoesNotExist:
        return JsonResponse({"error": "对话不存在或无权访问"}, status=404)

# 删除对话
@csrf_exempt
@require_http_methods(["POST"])
def delete_conversation_view(request, conversation_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "未登录"}, status=401)
    
    success = delete_conversation(conversation_id, request.user)
    if not success:
        return JsonResponse({"error": "对话不存在或无权访问"}, status=404)
    
    return JsonResponse({"status": "success"})

# 聊天界面
def deepseek_chat(request):
    if not request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('/login/')
    
    return render(request, 'Chat_interface.html', {
        'user': request.user
    })
