# from django.shortcuts import render
# from DailyAttendance import ormoperator
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from django.contrib import messages

# # @login_required保证这个接口只能由登录的用户来调用
# # Create your views here.
# # 在该文件中写功能函数，在urls.py中写上对应关系，在对应html文件中调用urls.py中的新命名
# @login_required
# def deep_seek(request):
#     return render(request, 'DeepSeek.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers.json import DjangoJSONEncoder
from .ormoperator import get_deepseek_response
from .models import Conversation, Message
from Userlogin.models import UserInfo
from django.contrib import messages
import json

@login_required
def deepseek_chat(request):
    return render(request, 'Chat_interface.html', {
        'user': request.user
    })

@login_required
def start_conversation(request):
    """创建新对话会话"""
    if request.method == 'POST':
        try:
            conversation = Conversation.objects.create(
                user=request.user,
                title="新对话"
            )
            return JsonResponse({
                'conversation_id': conversation.id,
                'title': conversation.title
            })
        except Exception as e:
            return JsonResponse({
                'error': f'创建对话失败: {str(e)}'
            }, status=500)
    return JsonResponse({'error': '无效请求'}, status=400)

@csrf_exempt
@login_required
def chat_api(request):
    """处理聊天请求"""
    if request.method == 'POST':
        conversation_id = request.POST.get('conversation_id')
        prompt = request.POST.get('prompt', '')
        
        if not conversation_id:
            return JsonResponse({'error': '缺少对话ID'}, status=400)
        
        # 传递当前用户对象
        response, tokens_used = get_deepseek_response(
            request.user, 
            conversation_id, 
            prompt
        )
        
        return JsonResponse({
            'response': response,
            'tokens_used': tokens_used
        })
    return JsonResponse({'error': '无效请求'}, status=400)

@login_required
def conversation_list_api(request):
    """API: 获取当前用户的对话列表"""
    conversations = Conversation.objects.filter(
        user=request.user
    ).order_by('-updated_at').values('id', 'title', 'created_at', 'updated_at')
    
    return JsonResponse(list(conversations), safe=False)

@login_required
def conversation_messages_api(request, conversation_id):
    """API: 获取特定对话的所有消息"""
    conversation = get_object_or_404(
        Conversation, 
        id=conversation_id,
        user=request.user
    )
    messages = conversation.messages.order_by('created_at').values('role', 'content', 'created_at')
    
    return JsonResponse({
        'id': conversation.id,
        'title': conversation.title,
        'messages': list(messages)
    }, encoder=DjangoJSONEncoder)

@login_required
def delete_conversation(request, conversation_id):
    """删除对话"""
    if request.method == 'POST':
        conversation = get_object_or_404(
            Conversation, 
            id=conversation_id,
            user=request.user
        )
        conversation.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        
        messages.success(request, f'对话 "{conversation.title}" 已删除')
        return redirect('conversation_list')
    
    return JsonResponse({'error': '无效请求'}, status=400)

# @login_required
# def start_conversation(request):
#     """创建新对话会话"""
#     try:
#         conversation = Conversation.objects.create(
#             user=request.user,
#             title="新对话"
#         )
#         return JsonResponse({
#             'conversation_id': conversation.id,
#             'title': conversation.title
#         })
#     except Exception as e:
#         return JsonResponse({
#             'error': f'创建对话失败: {str(e)}'
#         }, status=500)

# @csrf_exempt
# @login_required
# def chat_api(request):
#     """处理聊天请求"""
#     if request.method == 'POST':
#         conversation_id = request.POST.get('conversation_id')
#         prompt = request.POST.get('prompt', '')
        
#         if not conversation_id:
#             return JsonResponse({'error': '缺少对话ID'}, status=400)
        
#         # 传递当前用户对象
#         response, tokens_used = get_deepseek_response(
#             request.user, 
#             conversation_id, 
#             prompt
#         )
        
#         return JsonResponse({
#             'response': response,
#             'tokens_used': tokens_used
#         })
#     return JsonResponse({'error': '无效请求'}, status=400)

# @login_required
# def conversation_list(request):
#     """列出用户所有对话"""
#     conversations = Conversation.objects.filter(
#         user=request.user
#     ).order_by('-updated_at')
#     return render(request, 'qa/conversation_list.html', {
#         'conversations': conversations,
#         'user': request.user
#     })

# @login_required
# def conversation_detail(request, conversation_id):
#     """查看特定对话"""
#     conversation = get_object_or_404(
#         Conversation, 
#         id=conversation_id,
#         user=request.user
#     )
#     messages = conversation.messages.all().order_by('created_at')
#     return render(request, 'qa/conversation_detail.html', {
#         'conversation': conversation,
#         'messages': messages,
#         'user': request.user
#     })

# @login_required
# def delete_conversation(request, conversation_id):
#     """删除对话"""
#     conversation = get_object_or_404(
#         Conversation, 
#         id=conversation_id,
#         user=request.user
#     )
#     conversation.delete()
#     messages.success(request, f'对话 "{conversation.title}" 已删除')
#     return redirect('conversation_list')


#123