# 🏆 Gold Trading Calculator - Multi-Account MT5 System

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](./tests/)
[![Docker Support](https://img.shields.io/badge/docker-supported-blue.svg)](./deploy/docker/)
[![Security](https://img.shields.io/badge/security-jwt%20auth-green.svg)](#security)
[![Testing](https://img.shields.io/badge/testing-comprehensive-orange.svg)](./TESTING_GUIDE.md)

> **Professional Gold Trading Lot Calculator with Multi-Account MT5 Integration, Role-Based Authentication, and Advanced Risk Management**

## 🌟 Overview

The Gold Trading Calculator is a comprehensive trading system that combines precision lot size calculations with multi-account MetaTrader 5 integration. Built with security-first architecture, it supports multiple user roles, automated trade execution, and real-time market data integration.

### ✨ Key Features

- **🧮 Advanced Lot Calculator**: Precise position sizing for XAUUSD with multi-zone support
- **🔐 Multi-Account MT5**: Manage multiple MetaTrader 5 accounts per user
- **👥 Role-Based Access**: User, Broadcast, and Super Admin roles
- **🚀 Docker Deployment**: Complete containerization with production setup
- **🔒 JWT Authentication**: Secure API access with encrypted credentials
- **📊 Real-Time Data**: Live price feeds and account synchronization
- **🧪 Comprehensive Testing**: 60+ automated tests covering all functionality
- **🌐 REST API**: Full-featured API for external integrations

## 🏗️ Architecture

```
Gold Trading Calculator
├── Frontend (HTML/CSS/JS)
│   ├── Lot Calculator Interface
│   ├── Multi-Account Dashboard
│   └── Admin Broadcast System
├── Backend (Flask/Python)
│   ├── JWT Authentication
│   ├── MT5 Integration
│   ├── Role Management
│   └── Encrypted Storage
├── Database (SQLite)
│   ├── Users & Roles
│   ├── MT5 Accounts
│   ├── Trading Sessions
│   └── Audit Logs
└── Deployment
    ├── Docker Containers
    ├── Nginx Proxy
    └── Automated Testing
```

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/zicula/gold-trading-calculator.git
cd gold-trading-calculator

# Build and run with Docker
docker build -f deploy/docker/Dockerfile.simple -t gold-trading-calc .
docker run -d -p 8080:8080 --name gold-calc gold-trading-calc

# Or use Docker Compose for full stack
docker-compose -f deploy/docker/docker-compose.yml up -d
```

### Option 2: Local Development

```bash
# Setup Python environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the application
python backend/app.py
```

### Access the Application

- **Web Interface**: http://localhost:8080
- **API Documentation**: http://localhost:8080/api/status
- **Health Check**: http://localhost:8080/api/status

## 📋 API Overview

### Authentication Endpoints

```bash
# Register new user
POST /api/register
{
  "username": "trader1",
  "email": "trader1@example.com", 
  "password": "SecurePass123!"
}

# Login
POST /api/login
{
  "username": "trader1",
  "password": "SecurePass123!"
}
```

### MT5 Account Management

```bash
# Add MT5 account
POST /api/accounts
Authorization: Bearer <token>
{
  "account_name": "Live Account 1",
  "login": "12345678",
  "password": "mt5password",
  "server": "MetaQuotes-Demo"
}

# Connect to MT5
POST /api/accounts/<id>/connect
Authorization: Bearer <token>
```

### Trading Calculations

```bash
# Calculate lot size
POST /api/calculate
Authorization: Bearer <token>
{
  "symbol": "XAUUSD",
  "entryPrice1": "2000",
  "stopLoss": "1990", 
  "portfolioSize": "10000",
  "riskPercent": "2"
}
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: User, Broadcast, Super Admin roles
- **Password Encryption**: bcrypt with salt rounds
- **API Key Management**: Unique encrypted API keys per user
- **Audit Logging**: Complete audit trail of all activities
- **Rate Limiting**: Protection against API abuse
- **CORS Configuration**: Secure cross-origin resource sharing

## 🧪 Testing

Run comprehensive automated tests:

```bash
# Quick test (5 minutes)
./tests/quick_test.sh

# Full test suite (60+ tests)
./tests/run_tests.sh

# Frontend testing
# Follow guide in tests/FRONTEND_TESTING_CHECKLIST.md
```

### Test Coverage

- ✅ **Authentication**: Registration, login, JWT validation
- ✅ **Authorization**: Role-based access control
- ✅ **MT5 Integration**: Account management, connections
- ✅ **Calculations**: Lot sizing, risk management
- ✅ **Security**: Input validation, injection prevention
- ✅ **Performance**: Load testing, response times

## 🌐 Deployment Options

### 1. Production Docker (Recommended)

```bash
# Production deployment with full stack
docker-compose -f deploy/docker/docker-compose.yml up -d

# Includes:
# - Flask application
# - Redis cache
# - Nginx reverse proxy
# - Automated backups
```

### 2. DigitalOcean VPS

Follow the [DigitalOcean Setup Guide](./docs/guides/DIGITALOCEAN_SETUP_GUIDE.md)

### 3. Local Development Server

```bash
# Development mode with hot reload
export FLASK_ENV=development
python backend/app.py
```

## 📖 Documentation

- **[Getting Started Guide](./docs/guides/GETTING_STARTED.md)** - Complete setup instructions
- **[Testing Guide](./TESTING_GUIDE.md)** - Comprehensive testing methodology
- **[Deployment Guide](./docs/guides/DEPLOYMENT_GUIDE.md)** - Production deployment
- **[API Reference](./docs/api/)** - Complete API documentation
- **[Security Guide](./docs/guides/SECURITY.md)** - Security best practices

## 🔧 Configuration

### Environment Variables

```bash
# Security
export SECRET_KEY="your-secret-key"
export JWT_SECRET_KEY="your-jwt-secret"
export ENCRYPTION_KEY="your-encryption-key"

# Database
export DATABASE_PATH="trading_accounts.db"

# CORS
export CORS_ORIGINS="https://yourdomain.com"

# Rate Limiting
export API_RATE_LIMIT="100"  # requests per hour
export SESSION_TIMEOUT="24"  # hours
```

### Database Configuration

The system uses SQLite by default with the following tables:

- `users` - User accounts and roles
- `mt5_accounts` - MetaTrader 5 account credentials
- `trading_sessions` - Active trading sessions
- `audit_log` - Security and activity audit trail
- `broadcast_queue` - Admin broadcast messages

## 🎯 Use Cases

### Individual Traders
- Calculate optimal lot sizes for gold trading
- Manage multiple MT5 accounts
- Track trading performance

### Trading Firms
- Multi-user environment with role management
- Centralized MT5 account management
- Broadcast system for firm-wide communications

### Educational Institutions
- Teaching risk management concepts
- Demonstrating lot size calculations
- Safe environment for practice trading

## 🔄 Changelog

### Version 2.0.0 (Current)
- ✅ Multi-account MT5 integration
- ✅ JWT authentication system
- ✅ Role-based access control
- ✅ Docker containerization
- ✅ Comprehensive testing framework
- ✅ Production-ready security

### Version 1.0.0
- ✅ Basic lot size calculator
- ✅ XAUUSD trading support
- ✅ Risk management calculations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Run tests: `./tests/run_tests.sh`
4. Commit changes: `git commit -am 'Add new feature'`
5. Push to branch: `git push origin feature/new-feature`
6. Submit a Pull Request

### Development Guidelines

- Follow Python PEP 8 style guide
- Add tests for new features
- Update documentation
- Maintain security best practices

## 🐛 Troubleshooting

### Common Issues

**MetaTrader 5 Connection Fails**
```bash
# Check MT5 is running and Auto Trading is enabled
# Verify server settings and credentials
# Check firewall settings for port 8080
```

**Docker Build Fails**
```bash
# Use simplified Dockerfile for development
docker build -f deploy/docker/Dockerfile.simple -t gold-calc .
```

**Authentication Issues**
```bash
# Check JWT token validity
# Verify CORS settings
# Clear browser cache and cookies
```

## 📞 Support

- **Documentation**: [Full Documentation](./docs/)
- **Issues**: [GitHub Issues](https://github.com/zicula/gold-trading-calculator/issues)
- **Testing**: [Testing Guide](./TESTING_GUIDE.md)
- **Deployment**: [Deployment Guides](./docs/guides/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎖️ Acknowledgments

- MetaQuotes for MetaTrader 5 platform
- Flask community for the web framework
- Docker for containerization support
- All contributors and testers

---

**⚠️ Disclaimer**: This software is for educational and professional trading purposes. Always use proper risk management and test thoroughly before live trading.

**🔒 Security Note**: Never commit real trading credentials to version control. Use environment variables for sensitive data.

**📈 Trading Note**: Past performance does not guarantee future results. Trade responsibly and within your risk tolerance.
