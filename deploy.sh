#!/bin/bash

# 确保脚本在错误时停止
set -e

echo "开始部署SVG转JSON服务..."

# 检查Docker是否已安装
if ! command -v docker &> /dev/null; then
    echo "Docker未安装，正在安装..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
fi

# 检查Docker Compose是否已安装
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose未安装，正在安装..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 创建必要的目录
echo "创建项目目录..."
mkdir -p ~/forgeojson
cd ~/forgeojson
mkdir -p uploads
chmod 777 uploads

# 构建和启动服务
echo "构建和启动Docker服务..."
sudo systemctl start docker
sudo systemctl enable docker
docker-compose down
docker-compose up --build -d

# 等待服务启动
echo "等待服务启动..."
sleep 5

# 检查服务是否正常运行
if curl -s http://localhost:8881 > /dev/null; then
    echo "服务已成功启动！"
    echo "您可以通过访问 http://localhost:8881 使用该服务"
else
    echo "服务启动可能存在问题，请检查日志："
    docker-compose logs
fi

# 显示容器状态
echo "容器状态："
docker-compose ps
