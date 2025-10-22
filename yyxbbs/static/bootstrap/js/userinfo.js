// 标签页切换功能
function switchTab(tabName) {
    // 隐藏所有标签页
    document.querySelectorAll('.tab-pane').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 移除所有标签按钮的active类
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    
    // 显示选中的标签页
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // 激活选中的标签按钮
    event.currentTarget.classList.add('active');
    
    // 更新URL参数（不刷新页面）
    const url = new URL(window.location);
    url.searchParams.set('tab', tabName);
    window.history.replaceState({}, '', url);
}

// 刷新缓存函数
function refreshCache() {
    fetch('{% url "PersonInfo:refresh_cache" %}', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('数据已刷新！');
            location.reload();
        } else {
            alert('刷新失败，请重试');
        }
    })
    .catch(error => {
        console.error('刷新缓存失败:', error);
        alert('网络错误，请重试');
    });
}

// 获取CSRF token的函数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 页面加载时处理
document.addEventListener('DOMContentLoaded', function() {
    // 如果URL中有tab参数，激活对应的标签页
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get('tab');
    if (tabParam && tabParam !== '{{ active_tab }}') {
        const tabButton = document.querySelector(`[onclick="switchTab('${tabParam}')"]`);
        if (tabButton) {
            tabButton.click();
        }
    }
    
    // 为留言内容中的图片添加响应式类
    document.querySelectorAll('.comment-content img').forEach(img => {
        img.classList.add('img-fluid');
    });
});