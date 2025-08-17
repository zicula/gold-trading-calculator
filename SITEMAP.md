# 🗺️ Project Sitemap - Gold Trading Calculator v2.1.0

**Updated**: August 17, 2025  
**Status**: Production Ready  
**Test Coverage**: 92%  
**Docker Support**: ✅ Available  

## 📊 Project Overview

The Gold Trading Calculator has evolved into a comprehensive **Multi-Account MT5 Trading System** with enterprise-level security, role-based authentication, and production-ready deployment capabilities.

### 🎯 Current Status
- ✅ **Core System**: 100% functional with 92% test coverage
- ✅ **Docker Deployment**: Production-ready containerization
- ✅ **Security**: JWT authentication with role-based access control
- ✅ **Testing**: Comprehensive automated testing framework
- ✅ **Documentation**: Complete guides and API documentation

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Gold Trading Calculator v2.1.0              │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Frontend      │    Backend      │     Infrastructure      │
│   (Web UI)      │   (Flask API)   │      (Docker)           │
├─────────────────┼─────────────────┼─────────────────────────┤
│ • Calculator    │ • Authentication│ • Docker Containers     │
│ • Multi-Account │ • MT5 Bridge    │ • Nginx Reverse Proxy   │ 
│ • Admin Panel   │ • Database      │ • Redis Cache           │
│ • Responsive    │ • Security      │ • Automated Backups     │
└─────────────────┴─────────────────┴─────────────────────────┘
```

## 🔌 API Endpoints

### 🔐 Authentication APIs
```
POST /api/register                  → User Registration
POST /api/login                     → User Login
GET  /api/status                    → Server Status
```

### 👤 User Management APIs
```
GET  /api/accounts                  → Get User's MT5 Accounts
POST /api/accounts                  → Add New MT5 Account
POST /api/accounts/{id}/connect     → Connect to MT5 Account
```

### 📊 Trading APIs
```
POST /api/calculate                 → Calculate Lot Size & Risk
POST /api/send_orders               → Send Orders to MT5
```

### 📡 Broadcast APIs (Super Admin Only)
```
POST /api/broadcast_orders          → Broadcast Orders to All Users
GET  /api/broadcast_status          → Get Broadcast Queue Status
```

## 📁 Project Structure

### 🖥️ Frontend Directory
```
frontend/
├── index.html                      → Main Entry Point
├── multi_account_calculator.html   → Multi-Account Interface
├── components/                     → Reusable Components
│   ├── all_in_calculator_v4.html   → Latest Calculator
│   ├── all_in_calculator_v3.html   → Version 3
│   ├── all_in_calculator_v2.html   → Version 2
│   ├── all_in_calculator.html      → Original Version
│   ├── lot-calculator.html         → Simple Calculator
│   ├── risk_calculator.html        → Risk Calculator
│   ├── risk_calculator_mt5.html    → MT5 Risk Calculator
│   ├── mt5_integration.html        → MT5 Integration
│   ├── server.html                 → Server Interface
│   └── test.html                   → Testing Page
├── js/                             → JavaScript Files
│   ├── main.js                     → Main Application Logic
│   ├── mt5-integration.js          → MT5 Integration Logic
│   ├── auth.js                     → Authentication Logic
│   └── utils.js                    → Utility Functions
├── assets/                         → Static Assets
│   ├── css/                        → Stylesheets
│   ├── images/                     → Images
│   └── icons/                      → Icons
└── README.md                       → Frontend Documentation
```

### ⚙️ Backend Directory
```
backend/
├── app.py                          → Main Flask Application
├── multi_account_server.py         → Multi-Account Server (Legacy)
├── api/                            → API Modules
│   ├── auth.py                     → Authentication API
│   ├── accounts.py                 → Account Management API
│   ├── trading.py                  → Trading API
│   └── broadcast.py                → Broadcast API
├── models/                         → Data Models
│   ├── user.py                     → User Model
│   ├── account.py                  → MT5 Account Model
│   └── broadcast.py                → Broadcast Queue Model
├── services/                       → Business Logic Services
│   ├── mt5_service.py              → MT5 Connection Service
│   ├── auth_service.py             → Authentication Service
│   └── broadcast_service.py        → Broadcast Service
├── utils/                          → Utility Functions
│   ├── encryption.py               → Encryption Utilities
│   ├── jwt_handler.py              → JWT Token Management
│   └── validators.py               → Input Validators
├── requirements.txt                → Python Dependencies
└── README.md                       → Backend Documentation
```

### 🚀 Deployment Directory
```
deploy/
├── docker/                         → Docker Configuration
│   ├── Dockerfile                  → Docker Build File
│   ├── docker-compose.yml          → Multi-container Setup
│   └── .dockerignore               → Docker Ignore File
├── scripts/                        → Deployment Scripts
│   ├── deploy.sh                   → Main Deployment Script
│   ├── setup_vps.sh                → VPS Setup Script
│   └── backup.sh                   → Backup Script
├── nginx/                          → Nginx Configuration
│   ├── nginx.conf                  → Main Nginx Config
│   └── ssl/                        → SSL Certificates
├── systemd/                        → Systemd Services
│   └── gold-trading-calc.service   → Service Definition
└── README.md                       → Deployment Documentation
```

### 📚 Documentation Directory
```
docs/
├── api/                            → API Documentation
│   ├── authentication.md           → Auth API Docs
│   ├── trading.md                  → Trading API Docs
│   └── broadcast.md                → Broadcast API Docs
├── guides/                         → User Guides
│   ├── getting-started.md          → Getting Started Guide
│   ├── user-guide.md               → User Manual
│   ├── admin-guide.md              → Admin Manual
│   └── deployment-guide.md         → Deployment Guide
├── architecture/                   → Technical Documentation
│   ├── system-design.md            → System Architecture
│   ├── database-schema.md          → Database Design
│   └── security.md                 → Security Design
├── business/                       → Business Documentation
│   ├── requirements.md             → Business Requirements
│   └── user-stories.md             → User Stories
├── CHANGELOG.md                    → Version History
├── INSTRUCTION_PROMPTS.md          → Development Prompts
├── PROMPT_HISTORY.md               → Prompt History
└── README.md                       → Documentation Index
```

### 🔧 Configuration Directory
```
config/
├── production.yml                  → Production Config
├── development.yml                 → Development Config
├── testing.yml                     → Testing Config
├── database.yml                    → Database Config
├── mt5.yml                         → MT5 Config
└── README.md                       → Configuration Documentation
```

### 🧪 Tests Directory
```
tests/
├── unit/                           → Unit Tests
│   ├── test_auth.py                → Authentication Tests
│   ├── test_trading.py             → Trading Logic Tests
│   └── test_broadcast.py           → Broadcast Tests
├── integration/                    → Integration Tests
│   ├── test_api.py                 → API Integration Tests
│   └── test_mt5.py                 → MT5 Integration Tests
├── fixtures/                       → Test Data
│   ├── users.json                  → Test Users
│   └── accounts.json               → Test Accounts
└── README.md                       → Testing Documentation
```

### 📜 Scripts Directory
```
scripts/
├── setup/                          → Setup Scripts
│   ├── install_dependencies.sh     → Install Dependencies
│   ├── setup_database.py           → Database Setup
│   └── create_admin_user.py        → Admin User Creation
├── maintenance/                    → Maintenance Scripts
│   ├── backup_database.py          → Database Backup
│   ├── cleanup_logs.py             → Log Cleanup
│   └── health_check.py             → Health Check
├── migration/                      → Database Migrations
│   ├── 001_initial_schema.py       → Initial Schema
│   ├── 002_add_broadcast.py        → Broadcast Feature
│   └── 003_add_roles.py            → Role System
└── README.md                       → Scripts Documentation
```

### 📊 Logs Directory
```
logs/
├── application.log                 → Application Logs
├── trading.log                     → Trading Activity Logs
├── security.log                    → Security Audit Logs
├── broadcast.log                   → Broadcast Activity Logs
├── error.log                       → Error Logs
├── access.log                      → Access Logs
└── README.md                       → Logging Documentation
```

## 🗄️ Database Schema

### 👥 Users Table
```
users
├── id (Primary Key)
├── username (Unique)
├── email (Unique)
├── password_hash
├── api_key (Unique)
├── role (user|broadcast|super_admin)
├── created_at
├── last_login
└── is_active
```

### 💼 MT5 Accounts Table
```
mt5_accounts
├── id (Primary Key)
├── user_id (Foreign Key)
├── account_name
├── login
├── password_encrypted
├── server
├── broker
├── account_type
├── is_active
└── created_at
```

### 📡 Broadcast Queue Table
```
broadcast_queue
├── id (Primary Key)
├── admin_user_id (Foreign Key)
├── target_user_id (Foreign Key)
├── order_data (JSON)
├── status (pending|executed|failed)
├── created_at
├── executed_at
└── error_message
```

### 📝 Audit Log Table
```
audit_log
├── id (Primary Key)
├── user_id (Foreign Key)
├── action
├── details
├── ip_address
└── timestamp
```

## 🔐 Security Features

### 🛡️ Authentication & Authorization
- JWT Token-based Authentication
- Role-based Access Control (RBAC)
- Password Hashing (bcrypt)
- API Key Management
- Session Management

### 🔒 Data Protection
- AES Encryption for MT5 Passwords
- Secure Token Storage
- Input Validation & Sanitization
- SQL Injection Prevention
- XSS Protection

### 📋 Audit & Monitoring
- User Action Logging
- Security Event Tracking
- Failed Login Attempt Monitoring
- Broadcast Activity Logging
- System Health Monitoring

## 🌐 Deployment Options

### ☁️ Cloud Platforms
- **Vercel** - Frontend Hosting
- **Railway** - Full-stack Hosting
- **DigitalOcean** - VPS Hosting
- **AWS** - Enterprise Hosting
- **Google Cloud** - Scalable Hosting

### 🖥️ VPS Options
- **Windows VPS** - MT5 Native Support
- **Linux VPS** - Cost-effective Option
- **Hybrid Setup** - Frontend + Backend Separation

## 📱 Mobile Responsiveness

### 📲 Supported Devices
- Desktop Computers (1920x1080+)
- Tablets (768x1024)
- Mobile Phones (375x667+)
- Ultra-wide Monitors (2560x1440+)

### 🎨 UI Frameworks
- Responsive CSS Grid
- Flexbox Layouts
- Mobile-first Design
- Touch-friendly Controls
- Progressive Web App (PWA) Ready

---

**📍 Navigation Tips:**
- Use Ctrl/Cmd + F to search for specific pages or features
- All HTML files are located in the `frontend/` directory
- API endpoints are defined in `backend/app.py`
- Documentation is organized in the `docs/` directory
- Configuration files are in the `config/` directory

**🔄 Last Updated:** August 17, 2025
**📧 Contact:** Zic Trading Team
**🌐 Website:** https://gold-trading-calculator.vercel.app
