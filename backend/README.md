# Backend - Multi-Account MT5 Trading Server

## 📁 โครงสร้าง

```
backend/
├── api/                   # API endpoints
│   ├── __init__.py
│   ├── auth.py           # Authentication endpoints
│   ├── accounts.py       # MT5 account management
│   ├── calculator.py     # Risk calculation
│   └── broadcast.py      # Broadcast functionality
├── models/               # Database models
│   ├── __init__.py
│   ├── user.py          # User model
│   ├── account.py       # MT5 account model
│   └── broadcast.py     # Broadcast queue model
├── services/            # Business logic
│   ├── __init__.py
│   ├── mt5_service.py   # MT5 integration
│   ├── calculation_service.py # Risk calculations
│   └── broadcast_service.py   # Broadcast logic
├── utils/               # Utilities
│   ├── __init__.py
│   ├── security.py      # Security functions
│   ├── database.py      # Database utilities
│   └── validators.py    # Input validation
├── app.py              # Main Flask application
├── config.py           # Configuration management
└── README.md           # This file
```

## 🚀 การติดตั้ง

### 1. ติดตั้ง Dependencies
```bash
cd backend
pip install -r ../config/backend_requirements.txt
```

### 2. ตั้งค่า Environment
```bash
cp ../config/backend.env.example .env
# แก้ไข .env ตามต้องการ
```

### 3. เริ่มต้น Database
```bash
python -c "from app import init_database; init_database()"
```

### 4. เริ่มใช้งาน Server
```bash
python app.py
```

## 🔧 API Documentation

### Authentication
- `POST /api/register` - สมัครสมาชิก
- `POST /api/login` - เข้าสู่ระบบ

### Accounts Management
- `GET /api/accounts` - ดูบัญชี MT5
- `POST /api/accounts` - เพิ่มบัญชี MT5
- `POST /api/accounts/:id/connect` - เชื่อมต่อบัญชี

### Trading
- `POST /api/calculate` - คำนวณ lot size
- `POST /api/send_orders` - ส่งคำสั่งไป MT5

### Broadcast (Super Admin only)
- `POST /api/broadcast_orders` - ส่ง broadcast
- `GET /api/broadcast_status` - ดูสถานะ broadcast

## 🔐 Security Features

### Authentication
- JWT tokens with expiration
- Password hashing with bcrypt
- Role-based access control

### Data Protection
- MT5 password encryption
- Secure API key generation
- Input validation and sanitization

### Audit & Monitoring
- Comprehensive audit logging
- Failed login attempt tracking
- Broadcast action monitoring

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    api_key VARCHAR(255) UNIQUE,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

### MT5 Accounts Table
```sql
CREATE TABLE mt5_accounts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    account_name VARCHAR(100),
    login VARCHAR(50),
    password_encrypted TEXT,
    server VARCHAR(100),
    broker VARCHAR(100),
    account_type VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Broadcast Queue Table
```sql
CREATE TABLE broadcast_queue (
    id INTEGER PRIMARY KEY,
    admin_user_id INTEGER,
    target_user_id INTEGER,
    order_data TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP,
    executed_at TIMESTAMP,
    error_message TEXT,
    FOREIGN KEY (admin_user_id) REFERENCES users (id),
    FOREIGN KEY (target_user_id) REFERENCES users (id)
);
```

## 🔄 Development Workflow

### 1. เพิ่ม API Endpoint ใหม่
```python
# 1. สร้างไฟล์ใน api/
# 2. เพิ่ม route ใน app.py
# 3. เพิ่ม tests
# 4. อัปเดต documentation
```

### 2. แก้ไข Database Schema
```python
# 1. แก้ไข models/
# 2. สร้าง migration script
# 3. ทดสอบ migration
# 4. อัปเดต documentation
```

### 3. เพิ่ม Business Logic
```python
# 1. เพิ่มใน services/
# 2. เพิ่ม unit tests
# 3. Integration tests
# 4. Documentation
```

## 🧪 Testing

### Unit Tests
```bash
python -m pytest tests/backend/
```

### Integration Tests
```bash
python -m pytest tests/integration/
```

### API Tests
```bash
python -m pytest tests/api/
```

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8080/api/status
```

### Logs
```bash
tail -f ../logs/trading_server.log
```

### Database Monitoring
```bash
sqlite3 ../config/database.sqlite "SELECT COUNT(*) FROM users;"
```

## 🚀 Production Deployment

### Environment Variables
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_PATH=/opt/trading/data/database.sqlite
ENCRYPTION_KEY=your-encryption-key
CORS_ORIGINS=https://your-domain.com
PORT=8080
FLASK_ENV=production
```

### Systemd Service
```ini
[Unit]
Description=Gold Trading Calculator Backend
After=network.target

[Service]
Type=simple
User=trading
WorkingDirectory=/opt/trading/backend
ExecStart=/opt/trading/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```
