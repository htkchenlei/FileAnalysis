import os
from flask import Blueprint, request, jsonify
from models import db, FileRecord
from services.converter import convert_file
from services.ai_service import analyze_document, test_ai_connection
from services.url_service import convert_url_to_md
from config import Config, config_instance

api = Blueprint('api', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@api.route('/upload', methods=['POST'])
def upload_file():
    import os
    from datetime import datetime
    
    # 确保日志目录存在
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 日志文件路径
    log_file = os.path.join(log_dir, f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    # 打印日志文件路径，方便调试
    print(f"日志文件路径: {log_file}")
    
    def log(message):
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
    
    log("收到文件上传请求")
    
    if 'file' not in request.files:
        log("没有文件部分")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        log("没有选择文件")
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        log(f"不允许的文件类型: {file.filename}")
        return jsonify({'error': 'File type not allowed'}), 400
    
    # 获取项目名称
    project_name = request.form.get('project_name', file.filename)
    log(f"项目名称: {project_name}")
    
    # 保存文件
    original_filename = file.filename
    file_path = os.path.join(Config.UPLOAD_FOLDER, original_filename)
    log(f"保存文件到: {file_path}")
    
    # 确保上传目录存在
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
        log(f"创建上传目录: {Config.UPLOAD_FOLDER}")
    
    # 保存文件
    try:
        file.save(file_path)
        log(f"文件保存成功")
        print(f"文件保存成功: {file_path}")
    except Exception as e:
        log(f"文件保存失败: {str(e)}")
        print(f"文件保存失败: {str(e)}")
        return jsonify({'error': f'文件保存失败: {str(e)}'}), 500
    
    # 确保项目名称以.md结尾
    if not project_name.endswith('.md'):
        project_name += '.md'
    
    # 创建文件记录
    file_record = FileRecord(
        filename=project_name,
        original_name=original_filename,
        status='processing'
    )
    db.session.add(file_record)
    db.session.commit()
    log(f"创建文件记录成功，ID: {file_record.id}")
    
    # 同步处理文件转换
    try:
        log(f"开始处理文件: {file_path}")
        # 转换文件
        content = convert_file(file_path)
        log(f"文件转换成功，内容长度: {len(content)}")
        
        # 保存转换后的md文件
        md_file_path = os.path.join(Config.UPLOAD_FOLDER, project_name)
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        log(f"MD文件保存成功: {md_file_path}")
        print(f"MD文件保存成功: {md_file_path}")
        
        # 更新数据库
        file_record.content = content
        file_record.status = 'completed'
        db.session.commit()
        log(f"数据库更新成功，状态: completed")
        print(f"文件处理完成，状态更新为completed")
    except Exception as e:
        error_message = str(e)
        log(f"文件转换失败: {error_message}")
        print(f"文件转换失败: {error_message}")
        # 更新数据库
        file_record.status = 'failed'
        file_record.error_message = error_message
        db.session.commit()
        log(f"数据库更新成功，状态: failed")
        print(f"文件处理失败，状态更新为failed")
    finally:
        log(f"文件处理完成")
        print(f"文件处理结束")
    
    return jsonify({
        'id': file_record.id,
        'filename': file_record.filename,
        'status': file_record.status,
        'content': file_record.content,
        'error_message': file_record.error_message
    })

@api.route('/url', methods=['POST'])
def handle_url():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    url = data['url']
    project_name = data.get('project_name', f"url_{hash(url)}.md")
    
    # 创建文件记录
    file_record = FileRecord(
        filename=project_name,
        original_name=url,
        status='processing'
    )
    db.session.add(file_record)
    db.session.commit()
    
    # 立即返回，异步处理转换
    import threading
    def process_url():
        try:
            # 转换URL内容
            content = convert_url_to_md(url)
            file_record.content = content
            file_record.status = 'completed'
        except Exception as e:
            file_record.status = 'failed'
            file_record.error_message = str(e)
        finally:
            db.session.commit()
    
    # 启动线程处理URL转换
    thread = threading.Thread(target=process_url)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'id': file_record.id,
        'filename': file_record.filename,
        'status': file_record.status,
        'content': file_record.content,
        'error_message': file_record.error_message
    })

@api.route('/files', methods=['GET'])
def get_files():
    files = FileRecord.query.order_by(FileRecord.created_at.desc()).all()
    return jsonify([{
        'id': f.id,
        'filename': f.filename,
        'status': f.status,
        'created_at': f.created_at.isoformat()
    } for f in files])

@api.route('/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    file_record = FileRecord.query.get(file_id)
    if not file_record:
        return jsonify({'error': 'File not found'}), 404
    
    return jsonify({
        'id': file_record.id,
        'filename': file_record.filename,
        'content': file_record.content,
        'analysis': file_record.analysis,
        'status': file_record.status,
        'error_message': file_record.error_message,
        'created_at': file_record.created_at.isoformat()
    })

@api.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    file_record = FileRecord.query.get(file_id)
    if not file_record:
        return jsonify({'error': 'File not found'}), 404
    
    # 删除文件
    file_path = os.path.join(Config.UPLOAD_FOLDER, file_record.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # 删除记录
    db.session.delete(file_record)
    db.session.commit()
    
    return jsonify({'message': 'File deleted successfully'})

@api.route('/analyze/<int:file_id>', methods=['POST'])
def analyze_file(file_id):
    file_record = FileRecord.query.get(file_id)
    if not file_record:
        return jsonify({'error': 'File not found'}), 404
    
    if file_record.status != 'completed':
        return jsonify({'error': 'File is not completed'}), 400
    
    try:
        analysis = analyze_document(file_record.content)
        # 保存分析结果到数据库
        file_record.analysis = analysis
        db.session.commit()
        return jsonify({'analysis': analysis})
    except Exception as e:
        # 保存错误信息到数据库
        file_record.analysis = f"分析失败: {str(e)}"
        db.session.commit()
        return jsonify({'error': str(e)}), 500

@api.route('/config', methods=['GET'])
def get_config():
    return jsonify({
        'ai_api_url': config_instance.AI_API_URL,
        'ai_api_key': config_instance.AI_API_KEY,
        'ai_model': config_instance.AI_MODEL,
        'ai_prompt': config_instance.AI_PROMPT
    })

@api.route('/config', methods=['POST'])
def update_config():
    data = request.json
    
    # 更新配置
    if 'ai_api_url' in data:
        config_instance.AI_API_URL = data['ai_api_url']
    if 'ai_api_key' in data:
        config_instance.AI_API_KEY = data['ai_api_key']
    if 'ai_model' in data:
        config_instance.AI_MODEL = data['ai_model']
    if 'ai_prompt' in data:
        config_instance.AI_PROMPT = data['ai_prompt']
    
    # 保存配置到文件
    config_instance.save_config()
    
    return jsonify({'message': 'Config updated successfully'})

@api.route('/test-ai', methods=['GET'])
def test_ai():
    result = test_ai_connection()
    return jsonify(result)

@api.route('/test-upload', methods=['POST'])
def test_upload():
    print("=" * 50)
    print("测试上传端点被调用")
    print(f"请求方法: {request.method}")
    print(f"Content-Type: {request.content_type}")
    print(f"请求数据: {request.data}")
    print(f"文件列表: {list(request.files.keys())}")
    print("=" * 50)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    print(f"文件名: {file.filename}")
    print(f"文件大小: {file.content_length}")
    
    return jsonify({
        'message': '测试成功',
        'filename': file.filename
    })
