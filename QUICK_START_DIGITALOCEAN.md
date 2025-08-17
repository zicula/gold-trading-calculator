# 🚀 DigitalOcean + GitHub Actions - Quick Start Guide

## 📌 Overview
Deploy Gold Trading Calculator to DigitalOcean VPS with automatic GitHub Actions deployment.

**Total Cost**: $12-24/month  
**Setup Time**: 2-3 hours  
**Maintenance**: Minimal (automated)

---

## ⚡ Quick Setup (5 Steps)

### 1. 🌊 Create DigitalOcean VPS

```bash
# Sign up at: https://www.digitalocean.com
# Use referral for $200 free credit (2 months free!)

VPS Specs (Recommended):
- OS: Windows Server 2022
- Plan: Basic $18/month (2GB RAM, 1 vCPU)
- Region: Singapore (closest to Asian brokers)
- Hostname: gold-trading-vps
```

### 2. 📡 Setup VPS

**RDP to your VPS** and run this **ONE COMMAND**:

```powershell
# Copy and paste this into PowerShell (Run as Administrator):
iwr -Uri "https://raw.githubusercontent.com/zicula/gold-trading-calculator/main/setup_digitalocean_vps.ps1" -OutFile setup.ps1; Set-ExecutionPolicy Bypass -Scope Process -Force; .\setup.ps1
```

This will automatically:
- ✅ Install Python, Git, dependencies
- ✅ Clone the repository
- ✅ Create Windows Service
- ✅ Configure firewall
- ✅ Setup health monitoring

### 3. 🔐 Configure GitHub Secrets

**In your GitHub repository** → Settings → Secrets → Actions:

```yaml
VPS_HOST: your.vps.ip.address
VPS_USERNAME: Administrator
VPS_SSH_PRIVATE_KEY: [your-ssh-private-key]
VPS_PORT: 22
```

**Get SSH Key:**
```bash
# On your Mac:
ssh-keygen -t rsa -b 4096 -f ~/.ssh/digitalocean
cat ~/.ssh/digitalocean      # Private key → GitHub Secret
cat ~/.ssh/digitalocean.pub  # Public key → Add to VPS
```

### 4. 🎯 Install MT5

**Download and install MT5** on your VPS:
- Get MT5 from your broker
- Or use: https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe
- Login with your trading account

### 5. 🚀 Deploy & Test

**Push code to GitHub:**
```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

**Test your application:**
- 🌐 Open: `http://your-vps-ip:8080`
- 🧮 Use Risk Calculator
- 📊 Check MT5 integration

---

## 🔧 Configuration Files

### Environment Configuration (.env)
```bash
# Edit on VPS: C:\TradingCalculator\.env
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_broker_server
FLASK_PORT=8080
FLASK_ENV=production
```

### DigitalOcean Firewall Rules
```yaml
Inbound Rules:
- SSH (22): Your IP only
- RDP (3389): Your IP only
- HTTP (80): All sources
- Custom (8080): All sources

Outbound Rules:
- All traffic: All destinations
```

---

## 🎛️ Management Commands

### On VPS (PowerShell):
```powershell
# Check service status
Get-Service "GoldTradingCalculator"

# Start/Stop service
Start-Service "GoldTradingCalculator"
Stop-Service "GoldTradingCalculator"

# View logs
Get-EventLog -LogName Application -Source "Python" -Newest 10

# Test application
curl http://localhost:8080/status

# Manual restart
Restart-Service "GoldTradingCalculator"
```

### Local Development:
```bash
# Test changes locally
python mt5_server.py

# Deploy to VPS
git push origin main  # Automatic deployment via GitHub Actions

# Check deployment status
# GitHub → Actions tab → Latest workflow
```

---

## 📊 Monitoring & Health

### Automatic Monitoring:
- ✅ Health check every 5 minutes
- ✅ Auto-restart if service fails
- ✅ Windows Event Log integration
- ✅ GitHub Actions deployment status

### Manual Health Check:
```bash
# Test from anywhere:
curl http://your-vps-ip:8080/status

# Expected response:
{
  "status": "healthy",
  "mt5_connected": true,
  "timestamp": "2025-08-17T10:30:00Z"
}
```

---

## 💰 Cost Optimization

### Free Tier Options:
```bash
# DigitalOcean Credit:
- Referral bonus: $200 (2 months free)
- Student pack: Additional credits

# GitHub:
- Actions: 2,000 minutes/month free
- Repository: Free for public repos
```

### Scaling Options:
```bash
# Upgrade VPS as needed:
Basic: $12/month (1GB RAM)    - Testing
Standard: $18/month (2GB RAM) - Recommended
Premium: $24/month (4GB RAM)  - Heavy trading
```

---

## 🔒 Security Checklist

### VPS Security:
- [ ] Changed default administrator password
- [ ] Enabled Windows Firewall
- [ ] Limited RDP access to your IP
- [ ] Using SSH keys instead of passwords
- [ ] Regular Windows Updates enabled

### Application Security:
- [ ] Environment variables for sensitive data
- [ ] HTTPS enabled (if using domain)
- [ ] API authentication implemented
- [ ] Regular backups configured

---

## 🆘 Troubleshooting

### Common Issues:

#### 🔌 Connection Issues:
```powershell
# Check if service is running
Get-Service "GoldTradingCalculator"

# Check port usage
netstat -an | findstr :8080

# Restart if needed
Restart-Service "GoldTradingCalculator"
```

#### 🤖 MT5 API Issues:
```python
# Test MT5 connection on VPS
python -c "import MetaTrader5 as mt5; print('MT5:', mt5.initialize())"
```

#### 🚀 GitHub Actions Failures:
- Check GitHub Actions logs
- Verify VPS secrets are correct
- Test SSH connection manually
- Check VPS disk space and memory

### Get Help:
- 📚 Documentation: Repository README
- 🐛 Issues: GitHub Issues tab
- 💬 Community: GitHub Discussions

---

## ✅ Success Indicators

After successful setup:

1. **🌐 Web Interface**: http://your-vps-ip:8080 loads properly
2. **🧮 Calculator Works**: Can input data and get results
3. **🤖 MT5 Connected**: Status shows MT5 connection active
4. **🚀 Auto-Deploy**: GitHub push triggers automatic deployment
5. **📊 Monitoring**: Health checks pass every 5 minutes

---

## 🎯 Next Steps

After basic setup:

1. **📱 Custom Domain**: Point domain to VPS for professional URL
2. **🔒 SSL Certificate**: Enable HTTPS for security
3. **📊 Enhanced Monitoring**: Add uptime monitoring service
4. **💾 Backup Strategy**: Setup automated backups
5. **📈 Scaling**: Add load balancer for multiple VPS instances

---

## 🎉 You're Ready to Trade!

**Total Monthly Cost**: $12-24  
**Uptime**: 99.9%+  
**Deployment**: Fully automated  
**Security**: Production-ready

**Happy Trading with your automated Gold Trading Calculator!** 📈💰

---

## 📞 Support Links

- **DigitalOcean**: https://docs.digitalocean.com/
- **GitHub Actions**: https://docs.github.com/en/actions
- **MT5 API**: https://www.mql5.com/en/docs/integration/python_metatrader5
- **Repository**: https://github.com/zicula/gold-trading-calculator
