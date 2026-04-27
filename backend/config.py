import os
import json

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'files.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt', 'rtf'}
    
    # 配置文件路径
    CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.json')
    
    # 硅基流动大模型配置
    AI_API_URL = 'https://api.siliconflow.cn/v1/chat/completions'
    AI_API_KEY = ''
    AI_MODEL = 'deepseek-ai/deepseek-v3.1-terminus'
    AI_PROMPT = '''你是一个招标文件分析专家，请从以下Markdown内容中提取出以下关键信息：
1. 招标人：
2. 代理机构：
3. 开标日期：
4. 评分标准：
5. 其他重要信息：

请以结构化的形式输出，确保信息准确完整。'''
    
    def __init__(self):
        # 加载配置文件
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    # 更新配置
                    if 'AI_API_URL' in config_data:
                        self.AI_API_URL = config_data['AI_API_URL']
                    if 'AI_API_KEY' in config_data:
                        self.AI_API_KEY = config_data['AI_API_KEY']
                    if 'AI_MODEL' in config_data:
                        self.AI_MODEL = config_data['AI_MODEL']
                    if 'AI_PROMPT' in config_data:
                        self.AI_PROMPT = config_data['AI_PROMPT']
            except Exception as e:
                print(f"加载配置文件失败: {str(e)}")
    
    def save_config(self):
        """保存配置到文件"""
        config_data = {
            'AI_API_URL': self.AI_API_URL,
            'AI_API_KEY': self.AI_API_KEY,
            'AI_MODEL': self.AI_MODEL,
            'AI_PROMPT': self.AI_PROMPT
        }
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            print("配置保存成功")
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")

# 创建全局配置实例
config_instance = Config()
