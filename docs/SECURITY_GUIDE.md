# 🔒 Security Guide - Gold Trading Calculator

Comprehensive security documentation for the Gold Trading Calculator Multi-Account MT5 System.

## 🎯 Security Overview

The Gold Trading Calculator implements enterprise-level security with multiple layers of protection:

- **Authentication**: JWT-based token system with expiration
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: Fernet encryption for sensitive data
- **Input Validation**: Comprehensive sanitization and validation
- **Rate Limiting**: Protection against brute force attacks
- **Audit Logging**: Complete activity tracking

---

## 🔐 Authentication Security

### JWT Token Implementation

**Token Structure:**
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "user_id": 1,
    "username": "trader1",
    "role": "user",
    "account_id": 1,
    "exp": 1692270000,
    "iat": 1692183600
  },
  "signature": "HMACSHA256(base64UrlEncode(header) + '.' + base64UrlEncode(payload), secret)"
}
```

**Security Features:**
- **HMAC SHA-256** signature algorithm
- **24-hour expiration** (configurable)
- **Automatic refresh** mechanism
- **Secure secret rotation** capability

### Password Security

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter  
- At least one number
- At least one special character
- No common passwords (dictionary check)

**Password Storage:**
```python
# bcrypt with salt rounds (cost factor: 12)
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
```

**Password Validation Example:**
```python
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain number"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain special character"
    
    return True, "Password is valid"
```

---

## 👥 Role-Based Access Control (RBAC)

### Role Hierarchy

```
Super Admin (super_admin)
├── Full system access
├── User management
├── Broadcast management
├── System configuration
└── Audit log access

Broadcast User (broadcast)
├── Enhanced calculator features
├── MT5 account management
├── Receive broadcast orders
└── Trading history access

Regular User (user)
├── Basic calculator features
├── MT5 account management
└── Personal trading history
```

### Permission Matrix

| Feature | User | Broadcast | Super Admin |
|---------|------|-----------|-------------|
| Calculator | ✅ | ✅ | ✅ |
| MT5 Accounts | ✅ | ✅ | ✅ |
| Receive Broadcasts | ❌ | ✅ | ✅ |
| Send Broadcasts | ❌ | ❌ | ✅ |
| User Management | ❌ | ❌ | ✅ |
| System Settings | ❌ | ❌ | ✅ |
| Audit Logs | ❌ | ❌ | ✅ |

### Authorization Middleware

```python
def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_token_from_request()
            if not token:
                return jsonify({'error': 'Token required'}), 401
            
            try:
                payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
                user_role = payload.get('role')
                
                # Role hierarchy check
                if not has_permission(user_role, required_role):
                    return jsonify({'error': 'Insufficient permissions'}), 403
                
                return f(payload, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401
        
        return decorated_function
    return decorator
```

---

## 🔐 Data Encryption

### Sensitive Data Protection

**MT5 Credentials Encryption:**
```python
from cryptography.fernet import Fernet

# Generate encryption key (store securely)
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Encrypt MT5 password
def encrypt_password(password):
    encrypted_password = cipher_suite.encrypt(password.encode('utf-8'))
    return encrypted_password.decode('utf-8')

# Decrypt MT5 password
def decrypt_password(encrypted_password):
    decrypted_password = cipher_suite.decrypt(encrypted_password.encode('utf-8'))
    return decrypted_password.decode('utf-8')
```

**Database Storage:**
```sql
-- MT5 accounts table with encrypted passwords
CREATE TABLE mt5_accounts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    account_name VARCHAR(100) NOT NULL,
    login VARCHAR(50) NOT NULL,
    password_encrypted TEXT NOT NULL,  -- Fernet encrypted
    server VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Encryption Key Management

**Environment Variables:**
```bash
# Production environment
ENCRYPTION_KEY=gAAAAABhZ2V0X3NlY3VyZV9rZXlfaGVyZQ==
JWT_SECRET_KEY=your-256-bit-secret-here
SECRET_KEY=your-flask-secret-key-here
```

**Key Rotation Strategy:**
1. Generate new encryption key
2. Decrypt all data with old key
3. Re-encrypt with new key
4. Update environment variables
5. Restart application

---

## 🛡️ Input Validation & Sanitization

### SQL Injection Prevention

**Using Parameterized Queries:**
```python
# ✅ Safe - Parameterized query
def get_user_by_username(username):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

# ❌ Dangerous - String interpolation
def get_user_by_username_unsafe(username):
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    return cursor.fetchone()
```

**SQLAlchemy ORM Protection:**
```python
from sqlalchemy import text

# ✅ Safe with SQLAlchemy
user = session.query(User).filter(User.username == username).first()

# ✅ Safe with parameterized raw SQL
result = session.execute(
    text("SELECT * FROM users WHERE username = :username"),
    {"username": username}
)
```

### XSS Protection

**Output Escaping:**
```python
from markupsafe import escape

def safe_output(user_input):
    return escape(user_input)

# Example: "<script>alert('xss')</script>" 
# Becomes: "&lt;script&gt;alert('xss')&lt;/script&gt;"
```

**Content Security Policy (CSP):**
```python
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' fonts.googleapis.com; "
        "font-src 'self' fonts.gstatic.com; "
        "img-src 'self' data: blob:; "
        "connect-src 'self'"
    )
    return response
```

### Input Validation Schema

**Trading Calculator Validation:**
```python
from marshmallow import Schema, fields, validate

class CalculationSchema(Schema):
    symbol = fields.Str(required=True, validate=validate.OneOf(['XAUUSD', 'XAGUSD']))
    entryPrice1 = fields.Float(required=True, validate=validate.Range(min=0.01))
    stopLoss = fields.Float(required=True, validate=validate.Range(min=0.01))
    portfolioSize = fields.Float(required=True, validate=validate.Range(min=100))
    riskPercent = fields.Float(required=True, validate=validate.Range(min=0.1, max=100))
    direction = fields.Str(validate=validate.OneOf(['buy', 'sell']))

# Usage
schema = CalculationSchema()
try:
    result = schema.load(request.json)
except ValidationError as err:
    return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
```

---

## 🚫 Rate Limiting & DDoS Protection

### API Rate Limiting

**Implementation:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# Specific endpoint limits
@app.route('/api/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    pass

@app.route('/api/calculate', methods=['POST'])
@limiter.limit("60 per minute")
def calculate():
    pass
```

**Rate Limit Configuration:**
```python
RATELIMIT_STRATEGY = "fixed-window"
RATELIMIT_HEADERS_ENABLED = True
RATELIMIT_STORAGE_URL = "redis://localhost:6379"

# Custom rate limit messages
@limiter.request_filter
def whitelist_localhost():
    return request.remote_addr == "127.0.0.1"
```

### Nginx Rate Limiting

**nginx.conf Configuration:**
```nginx
# Rate limiting zones
limit_req_zone $binary_remote_addr zone=auth:10m rate=10r/m;
limit_req_zone $binary_remote_addr zone=api:10m rate=60r/m;
limit_req_zone $binary_remote_addr zone=general:10m rate=100r/h;

server {
    location /api/login {
        limit_req zone=auth burst=5 nodelay;
        proxy_pass http://backend;
    }
    
    location /api/calculate {
        limit_req zone=api burst=10 nodelay;
        proxy_pass http://backend;
    }
    
    location /api/ {
        limit_req zone=general burst=20 nodelay;
        proxy_pass http://backend;
    }
}
```

---

## 📊 Security Monitoring & Logging

### Audit Logging

**Database Schema:**
```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action VARCHAR(100) NOT NULL,
    resource VARCHAR(100),
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);
```

**Audit Implementation:**
```python
def log_user_action(user_id, action, resource=None, details=None):
    cursor.execute('''
        INSERT INTO audit_log (user_id, action, resource, ip_address, user_agent, details)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        action,
        resource,
        request.remote_addr,
        request.user_agent.string,
        json.dumps(details) if details else None
    ))
    conn.commit()

# Usage examples
log_user_action(user_id, "LOGIN", details={"success": True})
log_user_action(user_id, "MT5_ACCOUNT_ADDED", "mt5_accounts", {"account_id": account_id})
log_user_action(user_id, "CALCULATION", "calculator", {"symbol": "XAUUSD", "lot_size": 2.0})
```

### Security Alert System

**Failed Login Monitoring:**
```python
def monitor_failed_logins(username, ip_address):
    # Check failed attempts in last 15 minutes
    recent_failures = get_failed_attempts(username, ip_address, minutes=15)
    
    if recent_failures >= 5:
        # Lock account temporarily
        lock_account(username, duration=900)  # 15 minutes
        
        # Send security alert
        send_security_alert({
            'type': 'BRUTE_FORCE_ATTEMPT',
            'username': username,
            'ip_address': ip_address,
            'attempts': recent_failures
        })
        
        return True
    return False
```

**Suspicious Activity Detection:**
```python
def detect_suspicious_activity(user_id, action):
    # Check for unusual patterns
    patterns = [
        check_unusual_login_location(user_id),
        check_rapid_api_calls(user_id),
        check_unusual_calculation_patterns(user_id),
        check_multiple_mt5_connections(user_id)
    ]
    
    if any(patterns):
        log_security_event(user_id, "SUSPICIOUS_ACTIVITY", {
            'action': action,
            'patterns_detected': [p for p in patterns if p]
        })
```

---

## 🔍 Security Headers

### HTTP Security Headers

```python
@app.after_request
def set_security_headers(response):
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Enable XSS protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Strict transport security (HTTPS only)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' fonts.googleapis.com; "
        "font-src 'self' fonts.gstatic.com"
    )
    
    # Referrer policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    return response
```

### CORS Configuration

```python
from flask_cors import CORS

# Production CORS settings
CORS(app, 
     origins=['https://yourdomain.com'],
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE'],
     supports_credentials=True,
     max_age=86400
)
```

---

## 🧪 Security Testing

### Penetration Testing Checklist

#### Authentication Testing
- [ ] **Brute Force Protection**: Test rate limiting on login endpoints
- [ ] **Token Validation**: Test with expired, invalid, and malformed tokens
- [ ] **Session Management**: Test token refresh and logout functionality
- [ ] **Password Policy**: Test weak password rejection

#### Authorization Testing
- [ ] **Role Escalation**: Test access to higher-privilege endpoints
- [ ] **Horizontal Access**: Test access to other users' resources
- [ ] **Direct Object Reference**: Test direct access to resources by ID

#### Input Validation Testing
- [ ] **SQL Injection**: Test all input fields with SQL injection payloads
- [ ] **XSS Testing**: Test input fields with JavaScript payloads
- [ ] **File Upload**: Test malicious file uploads (if applicable)
- [ ] **Buffer Overflow**: Test with extremely large inputs

#### Infrastructure Testing
- [ ] **SSL/TLS**: Test certificate validity and encryption strength
- [ ] **Rate Limiting**: Test API rate limits and DDoS protection
- [ ] **Error Handling**: Test error messages for information disclosure
- [ ] **Directory Traversal**: Test for unauthorized file access

### Automated Security Scanning

**OWASP ZAP Integration:**
```bash
# Install OWASP ZAP
docker run -t owasp/zap2docker-stable zap-baseline.py \
    -t http://localhost:8080 \
    -J zap-report.json
```

**SQLMap Testing:**
```bash
# Test for SQL injection
sqlmap -u "http://localhost:8080/api/login" \
       --data="username=test&password=test" \
       --method=POST \
       --batch
```

**Nikto Web Scanner:**
```bash
# Scan for common vulnerabilities
nikto -h http://localhost:8080
```

---

## 🚨 Incident Response

### Security Incident Procedure

#### 1. **Detection & Analysis**
- Monitor security alerts and logs
- Analyze the scope and impact
- Classify incident severity

#### 2. **Containment**
- Isolate affected systems
- Revoke compromised tokens
- Block malicious IP addresses

#### 3. **Eradication**
- Remove malicious code or access
- Patch vulnerabilities
- Update security configurations

#### 4. **Recovery**
- Restore systems from clean backups
- Regenerate compromised secrets
- Implement additional monitoring

#### 5. **Lessons Learned**
- Document the incident
- Update security procedures
- Implement preventive measures

### Emergency Response Commands

```bash
# Emergency: Block all traffic
sudo iptables -A INPUT -j DROP

# Emergency: Stop application
docker-compose down

# Emergency: Revoke all JWT tokens
# Update JWT_SECRET_KEY in environment and restart

# Emergency: Database backup
docker exec db-container sqlite3 /app/data/trading_accounts.db ".backup /backup/emergency_$(date +%Y%m%d_%H%M%S).db"

# Emergency: Check for suspicious activity
tail -f /var/log/application.log | grep -E "(FAILED_LOGIN|SUSPICIOUS_ACTIVITY|ERROR)"
```

---

## 📋 Security Compliance

### Security Standards Compliance

#### OWASP Top 10 Protection

1. **A01: Broken Access Control** ✅
   - Role-based access control implemented
   - Token-based authentication
   - Resource-level authorization

2. **A02: Cryptographic Failures** ✅
   - Strong encryption (Fernet + bcrypt)
   - Secure key management
   - HTTPS enforcement

3. **A03: Injection** ✅
   - Parameterized queries
   - Input validation and sanitization
   - SQL injection prevention

4. **A04: Insecure Design** ✅
   - Security-first architecture
   - Threat modeling implemented
   - Secure development practices

5. **A05: Security Misconfiguration** ✅
   - Secure default configurations
   - Security headers implemented
   - Regular security updates

6. **A06: Vulnerable Components** ✅
   - Dependency scanning
   - Regular updates
   - Version pinning

7. **A07: Authentication Failures** ✅
   - Strong password policy
   - Account lockout protection
   - Secure session management

8. **A08: Software Integrity Failures** ✅
   - Code signing
   - Secure deployment pipeline
   - Integrity checks

9. **A09: Logging Failures** ✅
   - Comprehensive audit logging
   - Security event monitoring
   - Log integrity protection

10. **A10: Server-Side Request Forgery** ✅
    - Input validation
    - Whitelist approach
    - Network segmentation

### Regulatory Compliance

#### Data Protection (GDPR-like)
- **Data Minimization**: Only collect necessary data
- **Encryption**: All personal data encrypted
- **Access Controls**: Strict access limitations
- **Audit Trail**: Complete activity logging
- **Data Retention**: Configurable retention policies

#### Financial Services
- **Strong Authentication**: Multi-factor capable
- **Audit Logging**: Complete transaction trails
- **Data Encryption**: End-to-end protection
- **Access Controls**: Role-based segregation

---

## 🔧 Security Configuration

### Production Security Checklist

#### Application Security
- [ ] Change all default passwords and secrets
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure security headers
- [ ] Set up rate limiting
- [ ] Enable audit logging
- [ ] Configure CORS properly
- [ ] Implement input validation
- [ ] Set up monitoring and alerting

#### Infrastructure Security
- [ ] Update operating system and packages
- [ ] Configure firewall rules
- [ ] Disable unnecessary services
- [ ] Set up intrusion detection
- [ ] Configure log aggregation
- [ ] Implement backup procedures
- [ ] Set up monitoring dashboards
- [ ] Test disaster recovery procedures

#### Database Security
- [ ] Change default database passwords
- [ ] Enable database encryption
- [ ] Configure access controls
- [ ] Set up database auditing
- [ ] Implement backup encryption
- [ ] Configure connection limits
- [ ] Enable query logging
- [ ] Test backup restoration

---

**🛡️ Remember**: Security is an ongoing process, not a one-time setup. Regularly review and update your security measures to protect against evolving threats.

**📞 Security Contacts**: Report security issues immediately to the development team through secure channels.
