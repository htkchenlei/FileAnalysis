import requests
from markitdown import MarkItDown

def convert_url_to_md(url):
    """从URL获取内容并转换为Markdown"""
    try:
        # 获取网页内容
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        html_content = response.text
        
        # 使用markitdown转换为Markdown
        md = MarkItDown()
        result = md.convert_string(html_content)
        return result.text_content
    except Exception as e:
        raise Exception(f"URL转换失败: {str(e)}")
