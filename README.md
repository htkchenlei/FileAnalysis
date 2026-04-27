# 招标文件智能分析系统

一个基于Flask和Vue 3的智能招标文件分析系统，支持文件上传、URL分析、自动转换为Markdown格式，并使用大模型进行智能分析。

## 功能特性

- 📁 **文件上传**：支持PDF、DOCX、DOC、TXT、RTF格式文件上传
- 🌐 **URL分析**：支持直接输入网址进行分析
- 📄 **自动转换**：将文件自动转换为Markdown格式
- 🤖 **智能分析**：使用大模型对文档内容进行智能分析，提取关键信息
- 💾 **历史记录**：保存分析历史，方便查看和管理
- 📊 **系统配置**：支持配置大模型API参数

## 技术栈

### 后端
- Python 3.13+
- Flask 2.0+
- SQLAlchemy ORM
- MarkItDown (文件转换)
- Requests (API调用)

### 前端
- Vue 3
- Pinia (状态管理)
- Vue Router
- Axios (HTTP客户端)

## 安装说明

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/file-analysis-system.git
cd file-analysis-system
```

### 2. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 安装前端依赖

```bash
cd ../frontend
npm install
```

## 使用方法

### 1. 启动后端服务

```bash
cd backend
python app.py
```

后端服务将在 `http://127.0.0.1:5000` 运行。

### 2. 启动前端服务

```bash
cd frontend
npm run dev
```

前端服务将在 `http://localhost:5173` 运行（如果端口被占用，会自动使用其他端口）。

### 3. 访问系统

打开浏览器，访问前端服务地址，即可使用系统。

## 系统配置

1. 进入系统配置页面
2. 填写大模型API相关参数：
   - API URL：大模型API地址
   - API Key：大模型API密钥
   - 模型名称：使用的模型名称
   - 提示词：分析文档的提示词
3. 点击保存配置
4. 点击测试连接，确保配置正确

## 项目结构

```
file-analysis-system/
├── backend/              # 后端代码
│   ├── routes/           # API路由
│   ├── services/         # 服务层
│   ├── instance/         # 数据库文件
│   ├── uploads/          # 上传文件目录
│   ├── app.py            # 后端入口
│   ├── config.py         # 配置文件
│   ├── models.py         # 数据模型
│   └── requirements.txt  # 依赖文件
├── frontend/             # 前端代码
│   ├── src/              # 源代码
│   │   ├── components/   # 组件
│   │   ├── views/        # 页面
│   │   ├── stores/       # 状态管理
│   │   └── router/       # 路由
│   ├── index.html        # 入口HTML
│   └── package.json      # 依赖配置
└── README.md             # 项目说明
```

## 注意事项

- 文件大小限制：最大50MB
- 支持的文件格式：PDF、DOCX、DOC、TXT、RTF
- 大模型分析需要配置有效的API Key
- 系统使用SQLite数据库，数据存储在 `backend/instance/files.db`

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！