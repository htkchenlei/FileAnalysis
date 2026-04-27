from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db

# 先导入mammoth库，确保它可用
try:
    import mammoth
    print('Mammoth imported successfully!')
except ImportError as e:
    print('Failed to import mammoth:', str(e))

from routes.api import api

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)

# 启用CORS
CORS(app)

# 注册路由
app.register_blueprint(api, url_prefix='/api')

# 添加测试路由
@app.route('/test')
def test():
    print('测试路由被调用')
    return jsonify({'message': '测试成功'})

# 创建数据库表
with app.app_context():
    db.create_all()  # 只创建表，不删除现有表

if __name__ == '__main__':
    print('启动Flask应用...')
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
