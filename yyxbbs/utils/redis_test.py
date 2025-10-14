from django_redis import get_redis_connection
from django.core.cache import cache

def test_redis_connection():
    """测试Redis连接是否正常"""
    print("🔍 测试Redis连接...")
    
    try:
        # 测试默认缓存
        cache.set('django_test', 'Hello from Django!', 30)
        result = cache.get('django_test')
        print(f"✅ 默认缓存测试: {result}")
        
        # 测试Session缓存
        session_conn = get_redis_connection("session")
        session_conn.set('session_test', 'Session works!', ex=30)
        session_result = session_conn.get('session_test')
        print(f"✅ Session缓存测试: {session_result}")
        
        # 测试连接信息
        info = session_conn.info()
        print(f"✅ Redis版本: {info['redis_version']}")
        print("🎉 所有Redis连接测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ Redis连接失败: {e}")
        return False

# 在Django shell中运行测试
# python manage.py shell
# from utils.redis_test import test_redis_connection
# test_redis_connection()