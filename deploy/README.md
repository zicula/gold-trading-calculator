# Deployment & Infrastructure

## 📁 โครงสร้าง

```
deploy/
├── scripts/               # Deployment scripts
│   ├── setup_digitalocean_vps.ps1   # ตั้งค่า DigitalOcean VPS
│   ├── setup_windows_vps.bat        # ตั้งค่า Windows VPS
│   ├── setup_mt5.sh                 # ติดตั้ง MT5 (Linux)
│   ├── setup_mt5_macos.sh           # ติดตั้ง MT5 (macOS)
│   ├── deploy.sh                    # Script deploy หลัก
│   ├── start_vps_server.bat         # เริ่มต้น server บน VPS
│   └── fix_vercel_auth.sh           # แก้ไข Vercel authentication
├── configs/               # Configuration files
│   ├── netlify.toml       # Netlify configuration
│   ├── vercel.json        # Vercel configuration
│   ├── nginx.conf         # Nginx configuration
│   ├── gunicorn.conf.py   # Gunicorn configuration
│   └── systemd.service    # Systemd service configuration
├── docker/               # Docker configurations
│   ├── Dockerfile         # Docker image definition
│   ├── docker-compose.yml # Docker compose setup
│   └── nginx.conf         # Nginx for Docker
├── .github/              # GitHub Actions workflows
│   └── workflows/
│       └── deploy.yml     # CI/CD pipeline
└── README.md             # This file
```

## 🚀 Deployment Options

### 1. GitHub Pages (Frontend Only)
```bash
# อัตโนมัติผ่าน GitHub Actions
git push origin main
```

### 2. DigitalOcean VPS (Full Stack)
```bash
# ใช้ PowerShell script
./scripts/setup_digitalocean_vps.ps1

# หรือใช้ manual deployment
./scripts/deploy.sh
```

### 3. Docker Deployment
```bash
# Build และ run ด้วย Docker Compose
cd deploy/docker
docker-compose up -d
```

### 4. Cloud Platforms
- **Netlify**: ใช้ `configs/netlify.toml`
- **Vercel**: ใช้ `configs/vercel.json`
- **AWS/GCP/Azure**: Custom setup

## 🔧 Configuration Files

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /opt/trading/frontend;
    }
}
```

### Systemd Service
```ini
[Unit]
Description=Gold Trading Calculator
After=network.target

[Service]
Type=simple
User=trading
WorkingDirectory=/opt/trading
ExecStart=/opt/trading/venv/bin/python backend/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8080:8080"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
```

## 📋 Deployment Checklist

### Pre-deployment
- [ ] Code tested locally
- [ ] Environment variables configured
- [ ] Database schema updated
- [ ] SSL certificates ready
- [ ] Backup strategy in place

### During deployment
- [ ] Stop existing services
- [ ] Backup current data
- [ ] Deploy new code
- [ ] Run database migrations
- [ ] Start services
- [ ] Verify functionality

### Post-deployment
- [ ] Health checks passing
- [ ] Logs monitoring setup
- [ ] Performance monitoring
- [ ] Security audit
- [ ] User acceptance testing

## 🔐 Security Considerations

### SSL/TLS
```bash
# Generate SSL certificate
sudo certbot --nginx -d your-domain.com
```

### Firewall
```bash
# UFW rules
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 8080
sudo ufw enable
```

### Environment Variables
```bash
# Production environment
export SECRET_KEY="your-secret-key"
export JWT_SECRET_KEY="your-jwt-key"
export DATABASE_PATH="/opt/trading/data/database.sqlite"
export CORS_ORIGINS="https://your-domain.com"
```

## 📊 Monitoring & Logging

### Health Monitoring
```bash
# Check application status
curl http://localhost:8080/api/status

# Check service status
systemctl status trading-calculator
```

### Log Management
```bash
# Application logs
tail -f /opt/trading/logs/app.log

# System logs
journalctl -u trading-calculator -f

# Nginx logs
tail -f /var/log/nginx/access.log
```

### Performance Monitoring
```bash
# CPU and Memory usage
htop

# Disk usage
df -h

# Network connections
netstat -tulpn | grep :8080
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
name: Deploy to VPS
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /opt/trading
            git pull origin main
            ./deploy/scripts/deploy.sh
```

### Automated Testing
```bash
# Run tests before deployment
python -m pytest tests/
npm test
```

### Rollback Strategy
```bash
# Keep previous version
cp -r /opt/trading /opt/trading.backup

# Rollback if needed
mv /opt/trading.backup /opt/trading
systemctl restart trading-calculator
```

## 🛠️ Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check logs
journalctl -u trading-calculator -n 50

# Check configuration
python backend/app.py --check-config

# Verify permissions
ls -la /opt/trading
```

#### Database Issues
```bash
# Check database file
ls -la /opt/trading/data/database.sqlite

# Verify schema
sqlite3 /opt/trading/data/database.sqlite ".schema"

# Backup and restore
cp database.sqlite database.backup.sqlite
```

#### SSL Certificate Issues
```bash
# Renew certificate
sudo certbot renew

# Check certificate status
sudo certbot certificates
```

## 📚 Resources

- [DigitalOcean Documentation](https://docs.digitalocean.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
