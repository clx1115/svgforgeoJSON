# Gunicorn 配置文件
bind = "127.0.0.1:8000"  # Gunicorn监听的地址和端口
workers = 3  # 工作进程数，建议设置为 CPU核心数 * 2 + 1
worker_class = "sync"  # 工作进程类型
timeout = 120  # 超时时间
max_requests = 1000  # 每个工作进程处理的最大请求数
max_requests_jitter = 50  # 重启抖动，防止所有工作进程同时重启
accesslog = "/var/log/forgeojson/access.log"  # 访问日志
errorlog = "/var/log/forgeojson/error.log"  # 错误日志
loglevel = "info"  # 日志级别
