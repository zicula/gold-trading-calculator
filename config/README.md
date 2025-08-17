# Configuration Files

## 📁 โครงสร้าง

```
config/
├── environments/          # Environment-specific configs
│   ├── development.env    # Development environment
│   ├── staging.env        # Staging environment
│   └── production.env     # Production environment
├── backend_requirements.txt # Python dependencies
├── backend.env.example     # Backend environment template
├── .env.example           # General environment template
├── requirements.txt       # Legacy requirements file
└── README.md             # This file
```

## 🔧 Environment Configuration

### Backend Environment (.env)
```env
# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
ENCRYPTION_KEY=your-encryption-key-here

# Database
DATABASE_PATH=../config/database.sqlite

# CORS
CORS_ORIGINS=https://zicula.github.io,https://your-domain.com

# Application
API_RATE_LIMIT=100
SESSION_TIMEOUT=24
PORT=8080
FLASK_ENV=production

# Logging
LOG_LEVEL=INFO
LOG_FILE=../logs/trading_server.log

# MT5
MT5_TIMEOUT_SECONDS=30
MT5_MAX_CONNECTIONS=10
```

### Frontend Environment
```javascript
// config.js
const CONFIG = {
    API_BASE: 'http://localhost:8080/api', // Development
    // API_BASE: 'https://your-domain.com/api', // Production
    
    // Features
    BROADCAST_ENABLED: true,
    DEMO_MODE: false,
    
    // UI
    THEME: 'default',
    LANGUAGE: 'th',
    
    // Trading
    DEFAULT_SYMBOLS: ['XAUUSD', 'XAGUSD'],
    DEFAULT_RISK_PERCENT: 2,
    DEFAULT_PORTFOLIO_SIZE: 1000
};
```

## 📦 Dependencies

### Backend Requirements
```txt
Flask==2.3.3
flask-cors==4.0.0
PyJWT==2.8.0
bcrypt==4.0.1
cryptography==41.0.4
Werkzeug==2.3.7
MetaTrader5==5.0.45
python-dotenv==1.0.0
gunicorn==21.2.0
pytest==7.4.2
pytest-flask==1.2.0
requests==2.31.0
```

### Frontend Dependencies (if using npm)
```json
{
  "devDependencies": {
    "http-server": "^14.1.1",
    "live-server": "^1.2.2",
    "prettier": "^3.0.0",
    "eslint": "^8.0.0"
  }
}
```

## 🌍 Environment Templates

### Development (.env.development)
```env
FLASK_ENV=development
DEBUG=true
API_BASE=http://localhost:8080/api
DATABASE_PATH=../config/dev_database.sqlite
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Staging (.env.staging)
```env
FLASK_ENV=staging
DEBUG=false
API_BASE=https://staging.your-domain.com/api
DATABASE_PATH=../config/staging_database.sqlite
LOG_LEVEL=INFO
CORS_ORIGINS=https://staging.your-domain.com
```

### Production (.env.production)
```env
FLASK_ENV=production
DEBUG=false
API_BASE=https://your-domain.com/api
DATABASE_PATH=/opt/trading/data/database.sqlite
LOG_LEVEL=WARNING
CORS_ORIGINS=https://zicula.github.io,https://your-domain.com
```

## 🔐 Security Configuration

### Generate Secure Keys
```python
# Generate SECRET_KEY
import secrets
print(secrets.token_hex(32))

# Generate JWT_SECRET_KEY
print(secrets.token_urlsafe(32))

# Generate ENCRYPTION_KEY
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### Environment Variables Priority
1. System environment variables
2. `.env` file in backend directory
3. Config file defaults
4. Application defaults

## 📊 Database Configuration

### SQLite (Default)
```python
DATABASE_CONFIG = {
    'path': '../config/database.sqlite',
    'backup_path': '../config/backups/',
    'backup_retention_days': 30
}
```

### PostgreSQL (Optional)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/trading_db
```

### MySQL (Optional)
```env
DATABASE_URL=mysql://user:password@localhost:3306/trading_db
```

## 🚀 Deployment Configuration

### DigitalOcean VPS
```env
VPS_HOST=your-vps-ip
VPS_USER=trading
VPS_SSH_KEY_PATH=~/.ssh/trading_key
DOMAIN=your-domain.com
SSL_EMAIL=your-email@domain.com
```

### Docker Configuration
```env
DOCKER_IMAGE=gold-trading-calculator
DOCKER_TAG=latest
DOCKER_PORT=8080
DOCKER_NETWORK=trading-network
```

## 📝 Usage Examples

### Load Environment
```python
# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'database.sqlite')
    # ... other configs
```

### Validate Configuration
```python
# Validation script
def validate_config():
    required_vars = [
        'SECRET_KEY',
        'JWT_SECRET_KEY',
        'ENCRYPTION_KEY'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        raise ValueError(f"Missing required environment variables: {missing}")
    
    print("✅ Configuration validated successfully")
```

## 🔧 Maintenance

### Backup Configuration
```bash
# Backup all config files
tar -czf config_backup_$(date +%Y%m%d).tar.gz config/
```

### Update Dependencies
```bash
# Update Python packages
pip install --upgrade -r config/backend_requirements.txt
pip freeze > config/backend_requirements.txt

# Check for security vulnerabilities
pip audit
```

### Environment Sync
```bash
# Copy environment template
cp config/backend.env.example .env

# Sync environments
rsync -av config/environments/ /opt/trading/config/
```

## 📚 References

- [Flask Configuration](https://flask.palletsprojects.com/en/2.3.x/config/)
- [python-dotenv Documentation](https://python-dotenv.readthedocs.io/)
- [Environment Variables Best Practices](https://12factor.net/config)
