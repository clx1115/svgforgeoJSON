FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建上传目录
RUN mkdir -p uploads && \
    chmod 777 uploads

EXPOSE 8881

# 设置非root用户运行应用
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

CMD ["python", "app.py"]
