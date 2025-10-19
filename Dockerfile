# Dockerfile
# 单阶段构建，因为模型是预先训练并提交到 Git 的
FROM python:3.11-slim

WORKDIR /app

# 为安全起见，创建非 root 用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 安装运行时依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码 (从 'src' 目录)
COPY ./src /app/src

# 复制在本地训练并提交到 Git 的模型
COPY ./models /app/models/

# 更改文件所有权为非 root 用户
RUN chown -R appuser:appuser /app
USER appuser

# 环境变量，控制加载哪个模型
ENV MODEL_VERSION="v0.1"

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# 
# 运行应用，使用 'src.app' 作为模块路径
#
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]