# 🐳 DigitalOcean Docker Deployment Guide
# Gold Trading Calculator - Complete Setup Instructions

## 📋 Overview

ใช่ครับ! **DigitalOcean VPS สามารถใช้ Docker ได้อย่างสมบูรณ์** และเป็นตัวเลือกที่ดีเยี่ยมสำหรับ deploy Gold Trading Calculator

## 🌟 ข้อดีของการใช้ Docker บน DigitalOcean

### ✅ **ข้อดี:**
- **รองรับ Docker เต็มรูปแบบ** - ทั้ง Ubuntu และ CentOS
- **Performance ดีเยี่ยม** - SSD storage และ network ความเร็วสูง
- **ราคาประหยัด** - เริ่มต้น $12/เดือน
- **Easy Scaling** - สามารถ upgrade/downgrade ได้ง่าย
- **Backup อัตโนมัติ** - มี snapshot และ volume backup
- **Load Balancer** - รองรับ high availability
- **Monitoring** - มี built-in monitoring

### 💰 **ราคา:**
```
Basic:    $12/month  (1GB RAM, 1 vCPU, 25GB SSD)
Standard: $18/month  (2GB RAM, 1 vCPU, 50GB SSD) ⭐ แนะนำ
Premium:  $24/month  (4GB RAM, 2 vCPU, 80GB SSD)
```

## 🚀 Quick Start - ใช้งานใน 3 ขั้นตอน

### 1️⃣ **สร้าง DigitalOcean Droplet**
```bash
# เลือก Ubuntu 22.04 LTS
# เลือก plan $18/month (2GB RAM แนะนำ)
# เลือก datacenter ใกล้ที่สุด (Singapore สำหรับไทย)
# เพิ่ม SSH key สำหรับความปลอดภัย
```

### 2️⃣ **Upload โปรเจ็ค**
```bash
# คัดลอกโปรเจ็คไปยัง VPS
scp -r . user@your-vps-ip:~/gold-trading-calculator
ssh user@your-vps-ip
cd ~/gold-trading-calculator
```

### 3️⃣ **Deploy ด้วย Docker**
```bash
# รัน script deploy อัตโนมัติ
./deploy/docker/deploy_digitalocean.sh

# หรือ manual deployment
docker-compose -f deploy/docker/docker-compose.yml up -d
```

## 🐳 Docker Configuration ที่สร้างให้แล้ว

### 📁 **ไฟล์ที่สร้างให้:**
```
deploy/docker/
├── Dockerfile                      → Multi-stage build
├── docker-compose.yml              → Complete stack
├── nginx/nginx.conf                → Reverse proxy config
├── .dockerignore                   → Optimize build
└── deploy_digitalocean.sh          → One-click deployment
```

### 🏗️ **Stack ที่ include:**
- **Frontend:** Static files served by Nginx
- **Backend:** Python Flask API
- **Database:** SQLite with volume persistence
- **Cache:** Redis for sessions
- **Proxy:** Nginx with SSL/TLS
- **Backup:** Automated database backup
- **Monitoring:** Health checks และ auto-restart

## 📖 การใช้งาน Docker Commands

### 🎯 **Commands พื้นฐาน:**
```bash
# เริ่มต้น services ทั้งหมด
docker-compose -f deploy/docker/docker-compose.yml up -d

# ดู status ของ containers
docker-compose -f deploy/docker/docker-compose.yml ps

# ดู logs
docker-compose -f deploy/docker/docker-compose.yml logs -f

# Restart service เดียว
docker-compose -f deploy/docker/docker-compose.yml restart gold-trading-app

# หยุด services ทั้งหมด
docker-compose -f deploy/docker/docker-compose.yml down

# Rebuild และ restart
docker-compose -f deploy/docker/docker-compose.yml up -d --build
```

### 🔧 **Commands สำหรับ maintenance:**
```bash
# Database backup
docker exec gold-trading-calculator cp /app/data/trading_accounts.db /app/backup/

# ดู resource usage
docker stats

# เข้าไปใน container
docker exec -it gold-trading-calculator bash

# ดู logs ของ service เดียว
docker-compose -f deploy/docker/docker-compose.yml logs gold-trading-app
```

## 🔐 Security Features

### 🛡️ **ความปลอดภัยที่ configured:**
- **Nginx Rate Limiting** - ป้องกัน DDoS
- **SSL/TLS Encryption** - HTTPS อัตโนมัติ
- **Firewall Rules** - เปิดแค่ port ที่จำเป็น
- **Container Isolation** - แยก services
- **Non-root User** - รัน container ด้วย user ปกติ
- **Health Checks** - ตรวจสอบ service อัตโนมัติ

### 🔑 **Environment Variables:**
```env
SECRET_KEY=auto-generated-secure-key
JWT_SECRET_KEY=auto-generated-jwt-key
ENCRYPTION_KEY=auto-generated-encryption-key
REDIS_PASSWORD=auto-generated-redis-password
CORS_ORIGINS=https://yourdomain.com
```

## 📊 Monitoring & Backup

### 📈 **Monitoring:**
- **Health Checks** - ตรวจสอบ API ทุก 30 วินาที
- **Auto Restart** - restart อัตโนมัติเมื่อ service down
- **Log Rotation** - จัดการ logs อัตโนมัติ
- **Resource Monitoring** - ตรวจสอบ CPU/Memory

### 💾 **Backup:**
- **Database Backup** - สำรองข้อมูลทุก 1 ชั่วโมง
- **Volume Persistence** - ข้อมูลไม่หายเมื่อ restart
- **Snapshot Support** - ใช้ DigitalOcean snapshot
- **Log Backup** - เก็บ logs ไว้ 7 วัน

## 🌐 Domain & SSL Setup

### 🌍 **Custom Domain:**
```bash
# 1. Point domain A record to VPS IP
# 2. Update CORS_ORIGINS in .env
# 3. Generate SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# 4. Update nginx SSL paths
# 5. Restart nginx
docker-compose -f deploy/docker/docker-compose.yml restart nginx
```

### 🔒 **SSL Certificate:**
```bash
# Let's Encrypt (Free SSL)
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com

# Update nginx config
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./deploy/docker/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./deploy/docker/nginx/ssl/key.pem
```

## 🚨 Troubleshooting

### ❗ **Common Issues:**

#### 🔧 **Port Already in Use:**
```bash
# ตรวจสอบ process ที่ใช้ port
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443

# หยุด apache2 ถ้ามี
sudo systemctl stop apache2
sudo systemctl disable apache2
```

#### 🔧 **Permission Denied:**
```bash
# เพิ่ม user เข้า docker group
sudo usermod -aG docker $USER
newgrp docker

# Logout และ login ใหม่
```

#### 🔧 **Container Won't Start:**
```bash
# ดู error logs
docker-compose -f deploy/docker/docker-compose.yml logs

# ตรวจสอบ disk space
df -h

# ตรวจสอบ memory
free -h
```

#### 🔧 **Database Issues:**
```bash
# Backup ข้อมูลก่อน
docker exec gold-trading-calculator cp /app/data/trading_accounts.db /app/backup/

# Reset database
docker-compose -f deploy/docker/docker-compose.yml down
docker volume rm gold-trading-calculator_app_data
docker-compose -f deploy/docker/docker-compose.yml up -d
```

## 📞 Support & Resources

### 📚 **Documentation:**
- DigitalOcean Docker Guide: https://docs.digitalocean.com/products/droplets/how-to/install-docker/
- Docker Compose Reference: https://docs.docker.com/compose/
- Nginx Configuration: https://nginx.org/en/docs/

### 🆘 **Get Help:**
- Check logs: `docker-compose logs -f`
- Monitor resources: `docker stats`
- Test connectivity: `curl http://localhost/api/status`

---

## ✅ **สรุป:**

**ใช่ครับ! DigitalOcean VPS ใช้ Docker ได้อย่างสมบูรณ์** และเราได้สร้าง complete Docker setup ให้แล้ว ที่รวม:

✅ **Multi-container Architecture**
✅ **Production-ready Configuration** 
✅ **Security & SSL Support**
✅ **Automated Deployment Script**
✅ **Monitoring & Backup**
✅ **One-click Setup**

แค่รัน `./deploy/docker/deploy_digitalocean.sh` ก็สามารถ deploy ทั้งระบบได้เลย! 🚀
