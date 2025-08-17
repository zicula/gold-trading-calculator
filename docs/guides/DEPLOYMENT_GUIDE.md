# 🚀 Deployment Guide - Gold Trading Calculator

Comprehensive deployment guide for the Gold Trading Calculator Multi-Account MT5 System.

## 📋 Table of Contents

1. [Pre-deployment Checklist](#pre-deployment-checklist)
2. [Docker Deployment (Recommended)](#docker-deployment-recommended)
3. [Production VPS Deployment](#production-vps-deployment)
4. [Local Development Setup](#local-development-setup)
5. [Environment Configuration](#environment-configuration)
6. [SSL/HTTPS Setup](#sslhttps-setup)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

## ✅ Pre-deployment Checklist

### System Requirements

#### Minimum Requirements
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Docker-compatible system
- **RAM**: 2GB minimum, 4GB recommended
- **CPU**: 2 cores minimum, 4 cores recommended  
- **Storage**: 20GB available space
- **Network**: Public IP address, ports 80/443 accessible

#### Software Prerequisites
- **Docker**: 20.10+ and Docker Compose 2.0+
- **Git**: Latest version
- **SSL Certificate**: For HTTPS (Let's Encrypt recommended)

### Pre-deployment Validation
```bash
# Verify system compatibility
docker --version      # Should be 20.10+
docker-compose --version  # Should be 2.0+
git --version         # Any recent version

# Check available resources
free -h              # RAM availability
df -h                # Disk space
lscpu                # CPU information
```

### Testing Requirements
```bash
# Run comprehensive tests before deployment
./tests/quick_test.sh    # 5-minute validation
./tests/run_tests.sh     # Full test suite

# Required test results:
# ✅ 95%+ test pass rate
# ✅ All critical features working
# ✅ Security validations passed
```

## 🐳 Docker Deployment (Recommended)

### Option 1: Single Container (Development/Testing)

```bash
# 1. Clone the repository
git clone https://github.com/zicula/gold-trading-calculator.git
cd gold-trading-calculator

# 2. Build the Docker image
docker build -f deploy/docker/Dockerfile.simple -t gold-trading-calc:latest .

# 3. Run the container
docker run -d \
  --name gold-trading-calc \
  -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  gold-trading-calc:latest

# 4. Verify deployment
sleep 10
curl http://localhost:8080/api/status
```

### Option 2: Full Production Stack (Recommended)

```bash
# 1. Clone and prepare
git clone https://github.com/zicula/gold-trading-calculator.git
cd gold-trading-calculator

# 2. Configure environment
cp .env.example .env
# Edit .env with your production values

# 3. Deploy with Docker Compose
docker-compose -f deploy/docker/docker-compose.yml up -d --build

# 4. Verify all services
docker-compose -f deploy/docker/docker-compose.yml ps
```

---

## 🎯 Recommended Deployment Flow

### For Beginners:
1. **Vercel Dashboard** (Web interface)
2. **GitHub Pages** (Built-in GitHub)
3. **Netlify** (User-friendly)

### For Advanced Users:
1. **Vercel CLI** (After account setup)
2. **Netlify CLI** (Feature-rich)
3. **Custom Server** (Full control)

---

## 🔧 Current Project Status

Your project is already configured with:
- ✅ `vercel.json` - Vercel configuration
- ✅ `netlify.toml` - Netlify configuration  
- ✅ `.gitignore` - Clean repository
- ✅ `package.json` - Dependencies
- ✅ GitHub repository ready

**Just need to choose deployment method!**

---

## 🚀 Quick Start Commands

### If you have Vercel account:
```bash
vercel --prod
```

### If you prefer Netlify:
```bash
netlify deploy --prod --dir=.
```

### If you want GitHub Pages:
```bash
# Just enable in GitHub repository settings
# No commands needed!
```

---

## 📞 Support

If you continue having issues:
1. Check your GitHub account is verified
2. Ensure you have a valid email address
3. Try different browsers for authentication
4. Contact platform support if needed

**Remember**: The web app is already working at the current URL, these are just for getting your own deployment! 🎉
