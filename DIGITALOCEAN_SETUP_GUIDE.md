# 🌊 DigitalOcean + GitHub Actions Setup Guide
# Gold Trading Calculator - Complete Deployment Solution

## 📋 Overview

This guide walks you through setting up:
- DigitalOcean Windows VPS for MT5 trading
- GitHub Actions for automatic deployment
- Complete CI/CD pipeline for the Gold Trading Calculator

---

## 💰 Cost Breakdown

### DigitalOcean Windows VPS Pricing:
```
Basic Plan:    $12/month  (1GB RAM, 1 vCPU, 25GB SSD)
Standard Plan: $18/month  (2GB RAM, 1 vCPU, 50GB SSD) ⭐ Recommended
Premium Plan:  $24/month  (4GB RAM, 2 vCPU, 80GB SSD)

Additional Costs:
- Backup (+20% of droplet cost)
- Load Balancer: $12/month (if needed)
- Firewall: Free
- Monitoring: Free
```

### GitHub:
```
GitHub Free:     $0/month (sufficient for our needs)
GitHub Pro:      $4/month (advanced features)
GitHub Actions:  2,000 minutes/month free
```

**Total Monthly Cost: $12-24 (just the VPS)**

---

## 🚀 Step-by-Step Setup Guide

### Phase 1: DigitalOcean Account Setup

#### 1.1 Create DigitalOcean Account
```bash
# Sign up at: https://www.digitalocean.com
# Use referral link for $200 free credit (2 months free VPS)
# Verify email and add payment method
```

#### 1.2 Generate SSH Key (for secure access)
```bash
# On your Mac:
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
# Save as: ~/.ssh/digitalocean_rsa
# Copy public key: cat ~/.ssh/digitalocean_rsa.pub
```

#### 1.3 Create Windows Droplet
```yaml
OS: Windows Server 2022
Plan: Basic ($12/month) or Standard ($18/month)
Region: Singapore (closest to Asian brokers)
SSH Keys: Add your public key
Hostname: gold-trading-vps
Tags: trading, mt5, production
```

---

### Phase 2: VPS Initial Setup

#### 2.1 Connect to VPS
```bash
# Get VPS IP from DigitalOcean dashboard
# Connect via RDP (Remote Desktop)
# Default credentials will be emailed to you
```

#### 2.2 Install Required Software
```powershell
# Run in PowerShell as Administrator:

# 1. Install Chocolatey (Package Manager)
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# 2. Install Python
choco install python -y

# 3. Install Git
choco install git -y

# 4. Install Visual C++ Redistributable
choco install vcredist2019 -y

# 5. Refresh environment
refreshenv
```

#### 2.3 Setup Application Directory
```powershell
# Create application directory
mkdir C:\TradingCalculator
cd C:\TradingCalculator

# Clone the repository
git clone https://github.com/zicula/gold-trading-calculator.git .

# Install Python dependencies
pip install -r requirements.txt
```

---

### Phase 3: MT5 Installation

#### 3.1 Download and Install MT5
```powershell
# Download MT5 from your broker
# Or use the universal installer:
# https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5setup.exe

# Install to default location: C:\Program Files\MetaTrader 5
```

#### 3.2 Configure MT5 API
```powershell
# In MT5 Terminal:
# Tools → Options → Expert Advisors
# ✅ Allow algorithmic trading
# ✅ Allow DLL imports
# ✅ Allow imports of external experts

# Add your broker account and test connection
```

---

### Phase 4: GitHub Actions Setup

#### 4.1 Add VPS Secrets to GitHub
```bash
# Go to your GitHub repository
# Settings → Secrets and variables → Actions
# Add the following secrets:

VPS_HOST=your.vps.ip.address
VPS_USERNAME=Administrator
VPS_PASSWORD=your_vps_password
VPS_PORT=22
```

#### 4.2 Create Deployment Key
```powershell
# On VPS, generate deployment key:
ssh-keygen -t rsa -b 4096 -C "vps-deploy-key"
# Save as: C:\Users\Administrator\.ssh\deploy_rsa

# Add public key to GitHub:
# Repository → Settings → Deploy keys → Add deploy key
# Paste contents of deploy_rsa.pub
```

#### 4.3 Setup Automated Deployment
```powershell
# Create deployment script on VPS
# File: C:\TradingCalculator\deploy.bat

@echo off
echo Starting deployment...
cd C:\TradingCalculator

echo Stopping existing server...
taskkill /F /IM python.exe /T 2>nul

echo Pulling latest changes...
git pull origin main

echo Installing dependencies...
pip install -r requirements.txt

echo Starting server...
start /B python mt5_server.py

echo Deployment complete!
```

---

### Phase 5: Windows Service Setup (Optional)

#### 5.1 Install NSSM (Service Manager)
```powershell
choco install nssm -y
```

#### 5.2 Create Windows Service
```powershell
# Create service for MT5 server
nssm install "GoldTradingCalculator" "C:\Python39\python.exe"
nssm set "GoldTradingCalculator" AppDirectory "C:\TradingCalculator"
nssm set "GoldTradingCalculator" AppParameters "mt5_server.py"
nssm set "GoldTradingCalculator" DisplayName "Gold Trading Calculator MT5 Server"
nssm set "GoldTradingCalculator" Description "Automated trading calculator with MT5 integration"

# Start the service
net start GoldTradingCalculator

# Set to start automatically
sc config GoldTradingCalculator start=auto
```

---

### Phase 6: Firewall Configuration

#### 6.1 Windows Firewall
```powershell
# Allow Flask server port
New-NetFirewallRule -DisplayName "Flask MT5 Server" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow

# Allow RDP (if not already enabled)
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
```

#### 6.2 DigitalOcean Firewall
```bash
# In DigitalOcean Control Panel:
# Networking → Firewalls → Create Firewall

Inbound Rules:
- SSH (22): Your IP only
- RDP (3389): Your IP only  
- HTTP (80): All IPv4/IPv6
- HTTPS (443): All IPv4/IPv6
- Custom (8080): All IPv4/IPv6

Outbound Rules:
- All traffic: Allow all destinations
```

---

### Phase 7: SSL Certificate (Optional)

#### 7.1 Domain Setup
```bash
# If you have a domain, point it to your VPS IP
# Add A record: trading.yourdomain.com → your.vps.ip
```

#### 7.2 Install Certbot
```powershell
# For SSL certificate (if using domain)
choco install certbot -y

# Get certificate
certbot certonly --standalone -d trading.yourdomain.com
```

---

### Phase 8: Monitoring Setup

#### 8.1 Create Health Check Script
```powershell
# File: C:\TradingCalculator\health_check.ps1

$url = "http://localhost:8080/status"
try {
    $response = Invoke-WebRequest -Uri $url -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Server is healthy"
        exit 0
    }
} catch {
    Write-Host "❌ Server is down"
    # Restart service
    Restart-Service "GoldTradingCalculator"
    exit 1
}
```

#### 8.2 Schedule Health Checks
```powershell
# Create scheduled task for monitoring
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\TradingCalculator\health_check.ps1"
Register-ScheduledTask -TaskName "TradingCalculatorHealthCheck" -Trigger $trigger -Action $action
```

---

## 🔄 Usage Workflow

### Daily Development:
```bash
1. Code changes on local Mac
2. Push to GitHub repository
3. GitHub Actions automatically deploys to VPS
4. Test on VPS via browser: http://your-vps-ip:8080
5. MT5 receives orders automatically
```

### Monitoring:
```bash
# Check server status
curl http://your-vps-ip:8080/status

# View logs
# RDP to VPS → Check C:\TradingCalculator\logs\

# Restart if needed
# RDP to VPS → Restart Windows Service
```

---

## 🛠️ Troubleshooting

### Common Issues:

#### Connection Problems:
```powershell
# Check if service is running
Get-Service "GoldTradingCalculator"

# Check port usage
netstat -an | findstr :8080

# Restart service
Restart-Service "GoldTradingCalculator"
```

#### MT5 API Issues:
```python
# Test MT5 connection
python -c "import MetaTrader5 as mt5; print('MT5 Available:', mt5.initialize())"
```

#### GitHub Actions Failures:
```bash
# Check GitHub Actions logs
# Repository → Actions → Latest workflow run
# Debug SSH connection issues
```

---

## 📊 Performance Optimization

### VPS Optimization:
```powershell
# Disable unnecessary Windows services
# Disable Windows Defender (if interfering)
# Set high performance power plan
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c

# Optimize for trading applications
# Disable Windows Update automatic restart
# Configure timezone to match broker
```

### Application Optimization:
```python
# Enable production mode in Flask
export FLASK_ENV=production

# Use gunicorn for better performance
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 mt5_server:app
```

---

## 🔐 Security Best Practices

### VPS Security:
```powershell
# Change default administrator password
# Enable Windows Firewall
# Regular Windows Updates
# Use SSH keys instead of passwords
# Limit RDP access to your IP only
```

### Application Security:
```python
# Use environment variables for sensitive data
# Implement API authentication
# Enable CORS protection
# Use HTTPS in production
# Regular backup of trading data
```

---

## 📈 Scaling Options

### Vertical Scaling (Upgrade VPS):
```
Current: $12/month (1GB RAM)
Upgrade: $18/month (2GB RAM)
Premium: $24/month (4GB RAM)
```

### Horizontal Scaling:
```
Load Balancer: $12/month
Multiple VPS instances
Database separation
Microservices architecture
```

---

## 💾 Backup Strategy

### Automatic Backups:
```powershell
# Enable DigitalOcean automatic backups (+20% cost)
# Create weekly snapshots
# Backup trading data to external storage

# Backup script
robocopy C:\TradingCalculator C:\Backups\TradingCalculator /MIR /Z /XD .git
```

---

## 🎯 Next Steps

1. **Sign up for DigitalOcean** (use referral for free credit)
2. **Create Windows VPS** ($12-18/month)
3. **Follow setup guide** step by step
4. **Configure GitHub Actions** for auto-deployment
5. **Install MT5** and configure broker account
6. **Test the complete system**
7. **Enable monitoring** and backups

---

## 📞 Support

- **DigitalOcean Docs**: https://docs.digitalocean.com/
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **MT5 API Docs**: https://www.mql5.com/en/docs/integration/python_metatrader5

**Total Setup Time**: 2-4 hours
**Monthly Cost**: $12-24
**Maintenance**: Minimal (automated)
