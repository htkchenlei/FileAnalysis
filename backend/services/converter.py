import os
from markitdown import MarkItDown

def convert_file(file_path):
    """使用markitdown将文件转换为Markdown"""
    try:
        md = MarkItDown()
        result = md.convert(file_path)
        return result.text_content
    except Exception as e:
        raise Exception(f"转换失败: {str(e)}")
