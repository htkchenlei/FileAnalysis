import requests
from config import config_instance

def analyze_document(content):
    """使用大模型分析文档内容"""
    if not config_instance.AI_API_KEY:
        raise Exception("AI API Key 未配置，请在系统配置页面设置API Key")
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config_instance.AI_API_KEY}'
        }
        
        data = {
            'model': config_instance.AI_MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': config_instance.AI_PROMPT
                },
                {
                    'role': 'user',
                    'content': content
                }
            ],
            'temperature': 0.3
        }
        
        response = requests.post(config_instance.AI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        raise Exception(f"分析失败: {str(e)}")

def test_ai_connection():
    """测试大模型连接"""
    if not config_instance.AI_API_KEY:
        return {'status': 'error', 'message': 'AI API Key 未配置'}
    
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config_instance.AI_API_KEY}'
        }
        
        data = {
            'model': config_instance.AI_MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': '你是一个助手，请回复"测试成功"'
                },
                {
                    'role': 'user',
                    'content': '测试连接'
                }
            ],
            'temperature': 0.3
        }
        
        response = requests.post(config_instance.AI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        return {'status': 'success', 'message': '连接成功', 'response': result['choices'][0]['message']['content']}
    except Exception as e:
        return {'status': 'error', 'message': f'连接失败: {str(e)}'}
