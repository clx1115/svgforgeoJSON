# ForgeOJSON 部署指南

## 系统要求
- Linux系统（推荐Ubuntu 20.04或更新版本）
- Python 3.8+
- Nginx
- Systemd

## 部署步骤

### 1. 创建系统用户
```bash
sudo useradd -r -s /bin/false forgeojson
```

### 2. 创建项目目录
```bash
sudo mkdir -p /opt/forgeojson
sudo mkdir -p /var/log/forgeojson
sudo chown -R forgeojson:forgeojson /opt/forgeojson
sudo chown -R forgeojson:forgeojson /var/log/forgeojson
```

### 3. 复制项目文件
```bash
sudo cp -r * /opt/forgeojson/
sudo chown -R forgeojson:forgeojson /opt/forgeojson
```

### 4. 创建Python虚拟环境
```bash
cd /opt/forgeojson
sudo -u forgeojson python3 -m venv venv
sudo -u forgeojson venv/bin/pip install -r requirements.txt
```

### 5. 配置Nginx
```bash
# 编辑nginx配置文件中的域名
sudo nano /opt/forgeojson/nginx_forgeojson.conf

# 创建Nginx配置软链接
sudo ln -s /opt/forgeojson/nginx_forgeojson.conf /etc/nginx/sites-available/forgeojson
sudo ln -s /etc/nginx/sites-available/forgeojson /etc/nginx/sites-enabled/

# 测试Nginx配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

### 6. 配置Systemd服务
```bash
# 复制服务文件
sudo cp /opt/forgeojson/forgeojson.service /etc/systemd/system/

# 重新加载systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start forgeojson

# 设置开机自启
sudo systemctl enable forgeojson
```

### 7. 检查服务状态
```bash
# 检查服务状态
sudo systemctl status forgeojson

# 查看日志
sudo journalctl -u forgeojson
sudo tail -f /var/log/forgeojson/error.log
sudo tail -f /var/log/forgeojson/access.log
```

## 维护命令

### 重启服务
```bash
sudo systemctl restart forgeojson
```

### 停止服务
```bash
sudo systemctl stop forgeojson
```

### 查看日志
```bash
# 查看Gunicorn日志
sudo tail -f /var/log/forgeojson/error.log
sudo tail -f /var/log/forgeojson/access.log

# 查看Nginx日志
sudo tail -f /var/log/nginx/forgeojson_error.log
sudo tail -f /var/log/nginx/forgeojson_access.log
```

### 更新应用
```bash
# 进入项目目录
cd /opt/forgeojson

# 更新代码（假设使用git）
sudo -u forgeojson git pull

# 更新依赖
sudo -u forgeojson venv/bin/pip install -r requirements.txt

# 重启服务
sudo systemctl restart forgeojson
```

## 故障排除

1. 如果服务无法启动：
   - 检查日志: `sudo journalctl -u forgeojson`
   - 确认权限: `sudo chown -R forgeojson:forgeojson /opt/forgeojson`
   - 验证Python路径: `sudo -u forgeojson /opt/forgeojson/venv/bin/python -V`

2. 如果无法访问网站：
   - 检查Nginx状态: `sudo systemctl status nginx`
   - 检查Nginx日志: `sudo tail -f /var/log/nginx/error.log`
   - 确认防火墙设置: `sudo ufw status`
