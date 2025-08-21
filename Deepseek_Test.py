# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import requests
DEEPSEEK_API_KEY = "sk-e0894fd69b924b6f9fc4d501ca360f6b"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# client = OpenAI(api_key="sk-e0894fd69b924b6f9fc4d501ca360f6b", base_url="https://api.deepseek.com")
# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "1+2等于几？"},
#         {"role": "user", "content": "1+1等于几？"},
#     ],
#     stream=False
# )

# print(response.choices[0].message.content)

        
# 构建历史消息
message_history = []
message_history.append({"role": "user", "content": "1+1等于几"})

headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "deepseek-chat",
    "messages": message_history,
    "temperature": 0.7,
    "max_tokens": 2000
}

response = requests.post(
    DEEPSEEK_API_URL,
    headers=headers,
    json=payload,
    timeout=30  # 设置超时时间
)
response.raise_for_status()

# 解析响应
response_data = response.json()
assistant_reply = response_data['choices'][0]['message']['content']
tokens_used = response_data['usage']['total_tokens']
print(assistant_reply)