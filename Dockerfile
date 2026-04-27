# 使用Python 3.13作为基础镜像
FROM python:3.13-slim-bookworm

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 创建工作目录
WORKDIR /app

# 复制后端依赖文件
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制前端依赖文件
COPY frontend/package.json frontend/package-lock.json ./frontend/

# 安装前端依赖
WORKDIR /app/frontend
RUN npm install

# 复制前端代码
COPY frontend/ .

# 构建前端项目
RUN npm run build

# 复制后端代码
WORKDIR /app
COPY backend/ .

# 复制前端构建产物到后端静态目录
RUN mkdir -p static \
    && cp -r frontend/dist/* static/

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "app.py"]