#!/usr/bin/env python3
"""
Multi-Account MT5 Trading Server with Security
Support for multiple MT5 accounts per user with JWT authentication
"""

import os
import jwt  # PyJWT library provides 'jwt' module
import bcrypt
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from cryptography.fernet import Fernet
import logging
import hashlib
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

try:
    import MetaTrader5 as mt5
except ImportError:
    print("⚠️ MetaTrader5 not available, using mock mode")
    mt5 = None

# Initialize Flask app
app = Flask(__name__)

# Configuration
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'trading_accounts.db')
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://zicula.github.io').split(',')
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', '100'))  # requests per hour
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '24'))  # hours

app.config.from_object(Config)

# Setup CORS
CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize encryption
cipher_suite = Fernet(Config.ENCRYPTION_KEY)

# Database initialization
def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            api_key VARCHAR(255) UNIQUE NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    ''')
    
    # MT5 Accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mt5_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_name VARCHAR(100) NOT NULL,
            login VARCHAR(50) NOT NULL,
            password_encrypted TEXT NOT NULL,
            server VARCHAR(100) NOT NULL,
            broker VARCHAR(100),
            account_type VARCHAR(20) DEFAULT 'demo',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Trading sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trading_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_id INTEGER NOT NULL,
            session_token VARCHAR(255) NOT NULL,
            ip_address VARCHAR(45),
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (account_id) REFERENCES mt5_accounts (id)
        )
    ''')
    
    # Audit log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action VARCHAR(100) NOT NULL,
            details TEXT,
            ip_address VARCHAR(45),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Broadcast queue table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS broadcast_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_user_id INTEGER NOT NULL,
            target_user_id INTEGER NOT NULL,
            order_data TEXT NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            executed_at TIMESTAMP,
            error_message TEXT,
            FOREIGN KEY (admin_user_id) REFERENCES users (id),
            FOREIGN KEY (target_user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

# Security utilities
def encrypt_password(password):
    """Encrypt MT5 password for storage"""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    """Decrypt MT5 password for use"""
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def generate_api_key():
    """Generate secure API key for user"""
    return secrets.token_urlsafe(32)

def log_audit(user_id, action, details=None, ip_address=None):
    """Log user actions for security auditing"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO audit_log (user_id, action, details, ip_address)
        VALUES (?, ?, ?, ?)
    ''', (user_id, action, details, ip_address))
    conn.commit()
    conn.close()

# JWT token management
def generate_jwt_token(user_id, account_id=None):
    """Generate JWT token for user session"""
    payload = {
        'user_id': user_id,
        'account_id': account_id,
        'exp': datetime.utcnow() + timedelta(hours=Config.SESSION_TIMEOUT),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def verify_jwt_token(token):
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Authentication decorators
def require_auth(f):
    """Decorator to require authentication for API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            token = request.json.get('token') if request.json else None
        
        if not token:
            return jsonify({'error': 'Authentication token required'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        request.user_id = payload['user_id']
        request.account_id = payload.get('account_id')
        
        return f(*args, **kwargs)
    return decorated_function

def require_role(required_role):
    """Decorator to require specific role for API endpoints"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'user_id'):
                return jsonify({'error': 'Authentication required'}), 401
            
            conn = sqlite3.connect(Config.DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT role FROM users WHERE id = ?', (request.user_id,))
            user = cursor.fetchone()
            conn.close()
            
            if not user or user[0] != required_role:
                return jsonify({'error': f'Access denied. {required_role} role required'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_user_role(user_id):
    """Get user role from database"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

# MT5 Connection Manager
class MT5Manager:
    def __init__(self):
        self.connections = {}  # Cache for MT5 connections
    
    def connect_account(self, account_data):
        """Connect to specific MT5 account"""
        if not mt5:
            return self._mock_connection()
        
        account_key = f"{account_data['login']}_{account_data['server']}"
        
        try:
            # Disconnect any existing connection
            if account_key in self.connections:
                mt5.shutdown()
            
            # Decrypt password
            password = decrypt_password(account_data['password_encrypted'])
            
            # Initialize MT5 connection
            if not mt5.initialize():
                logger.error(f"Failed to initialize MT5 for account {account_data['login']}")
                return None
            
            # Login to account
            login_result = mt5.login(
                login=int(account_data['login']),
                password=password,
                server=account_data['server']
            )
            
            if login_result:
                self.connections[account_key] = {
                    'login': account_data['login'],
                    'server': account_data['server'],
                    'connected_at': datetime.now()
                }
                logger.info(f"Successfully connected to MT5 account {account_data['login']}")
                return account_key
            else:
                logger.error(f"Failed to login to MT5 account {account_data['login']}")
                return None
                
        except Exception as e:
            logger.error(f"Error connecting to MT5 account {account_data['login']}: {str(e)}")
            return None
    
    def _mock_connection(self):
        """Mock connection for development/testing"""
        return "mock_connection"
    
    def disconnect_account(self, account_key):
        """Disconnect from MT5 account"""
        if account_key in self.connections:
            if mt5:
                mt5.shutdown()
            del self.connections[account_key]
            logger.info(f"Disconnected from MT5 account {account_key}")

# Initialize MT5 manager
mt5_manager = MT5Manager()

# Static file routes for Railway deployment
@app.route('/')
def index():
    """Serve the main index.html"""
    from flask import send_from_directory
    return send_from_directory('../', 'index.html')

@app.route('/gold-trading-calculator/menu')
def menu():
    """Serve the menu page"""
    from flask import send_from_directory
    return send_from_directory('../', 'menu.html')

@app.route('/gold-trading-calculator/')
def calculator_index():
    """Serve calculator index (redirect to menu)"""
    from flask import send_from_directory
    return send_from_directory('../', 'menu.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files"""
    from flask import send_from_directory
    try:
        return send_from_directory('../', filename)
    except FileNotFoundError:
        return {"error": "File not found"}, 404

# API Routes

@app.route('/api/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')  # Default role is 'user'
        
        # Validate role
        valid_roles = ['user', 'broadcast', 'super_admin']
        if role not in valid_roles:
            role = 'user'
        
        if not all([username, email, password]):
            return jsonify({'error': 'Username, email, and password required'}), 400
        
        # Hash password
        password_hash = generate_password_hash(password)
        api_key = generate_api_key()
        
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, api_key, role)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, api_key, role))
            user_id = cursor.lastrowid
            conn.commit()
            
            log_audit(user_id, 'user_registered', f'Username: {username}, Role: {role}', request.remote_addr)
            
            return jsonify({
                'message': 'User registered successfully',
                'user_id': user_id,
                'api_key': api_key,
                'role': role
            }), 201
            
        except sqlite3.IntegrityError as e:
            return jsonify({'error': 'Username or email already exists'}), 409
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({'error': 'Username and password required'}), 400
        
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, password_hash, is_active, role FROM users 
            WHERE username = ? OR email = ?
        ''', (username, username))
        
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user[1], password):
            log_audit(None, 'login_failed', f'Username: {username}', request.remote_addr)
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user[2]:  # is_active
            return jsonify({'error': 'Account disabled'}), 403
        
        user_id = user[0]
        user_role = user[3]
        
        # Update last login
        cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', (datetime.now(), user_id))
        conn.commit()
        conn.close()
        
        # Generate JWT token
        token = generate_jwt_token(user_id)
        
        log_audit(user_id, 'user_login', None, request.remote_addr)
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user_id': user_id,
            'role': user_role
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/accounts', methods=['GET'])
@require_auth
def get_accounts():
    """Get user's MT5 accounts"""
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, account_name, login, server, broker, account_type, is_active, created_at
            FROM mt5_accounts 
            WHERE user_id = ? AND is_active = TRUE
        ''', (request.user_id,))
        
        accounts = []
        for row in cursor.fetchall():
            accounts.append({
                'id': row[0],
                'account_name': row[1],
                'login': row[2],
                'server': row[3],
                'broker': row[4],
                'account_type': row[5],
                'is_active': row[6],
                'created_at': row[7]
            })
        
        conn.close()
        return jsonify({'accounts': accounts}), 200
        
    except Exception as e:
        logger.error(f"Get accounts error: {str(e)}")
        return jsonify({'error': 'Failed to get accounts'}), 500

@app.route('/api/accounts', methods=['POST'])
@require_auth
def add_account():
    """Add new MT5 account"""
    try:
        data = request.json
        required_fields = ['account_name', 'login', 'password', 'server']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Encrypt password
        encrypted_password = encrypt_password(data['password'])
        
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO mt5_accounts 
            (user_id, account_name, login, password_encrypted, server, broker, account_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.user_id,
            data['account_name'],
            data['login'],
            encrypted_password,
            data['server'],
            data.get('broker', ''),
            data.get('account_type', 'demo')
        ))
        
        account_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        log_audit(request.user_id, 'account_added', f'Account: {data["account_name"]}', request.remote_addr)
        
        return jsonify({
            'message': 'Account added successfully',
            'account_id': account_id
        }), 201
        
    except Exception as e:
        logger.error(f"Add account error: {str(e)}")
        return jsonify({'error': 'Failed to add account'}), 500

@app.route('/api/accounts/<int:account_id>/connect', methods=['POST'])
@require_auth
def connect_account(account_id):
    """Connect to specific MT5 account"""
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Verify account belongs to user
        cursor.execute('''
            SELECT login, password_encrypted, server, account_name
            FROM mt5_accounts 
            WHERE id = ? AND user_id = ? AND is_active = TRUE
        ''', (account_id, request.user_id))
        
        account = cursor.fetchone()
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        # Prepare account data
        account_data = {
            'login': account[0],
            'password_encrypted': account[1],
            'server': account[2],
            'account_name': account[3]
        }
        
        # Connect to MT5
        connection_key = mt5_manager.connect_account(account_data)
        
        if connection_key:
            # Generate new token with account context
            token = generate_jwt_token(request.user_id, account_id)
            
            log_audit(request.user_id, 'account_connected', f'Account ID: {account_id}', request.remote_addr)
            
            return jsonify({
                'message': 'Connected successfully',
                'token': token,
                'account_id': account_id,
                'connection_key': connection_key
            }), 200
        else:
            return jsonify({'error': 'Failed to connect to MT5 account'}), 500
            
        conn.close()
        
    except Exception as e:
        logger.error(f"Connect account error: {str(e)}")
        return jsonify({'error': 'Connection failed'}), 500

@app.route('/api/calculate', methods=['POST'])
@require_auth
def calculate_risk():
    """Calculate lot size and risk"""
    try:
        if not request.account_id:
            return jsonify({'error': 'Account not connected'}), 400
        
        data = request.json
        
        # Validate required fields
        required = ['symbol', 'entryPrice1', 'stopLoss', 'portfolioSize', 'riskPercent']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing required calculation fields'}), 400
        
        # Perform calculations (same logic as before)
        portfolio_size = float(data['portfolioSize'])
        risk_percent = float(data['riskPercent'])
        entry_price = float(data['entryPrice1'])
        stop_loss = float(data['stopLoss'])
        
        risk_amount = portfolio_size * (risk_percent / 100)
        stop_distance = abs(entry_price - stop_loss)
        contract_size = 100  # oz per lot for Gold
        lot_size = risk_amount / (contract_size * stop_distance)
        
        # Log calculation
        log_audit(request.user_id, 'risk_calculated', 
                  f'Symbol: {data["symbol"]}, Lot: {lot_size:.4f}', 
                  request.remote_addr)
        
        return jsonify({
            'symbol': data['symbol'],
            'lotSize': round(lot_size, 4),
            'riskAmount': risk_amount,
            'stopDistance': stop_distance,
            'entryPrice': entry_price,
            'stopLoss': stop_loss,
            'calculatedAt': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Calculate error: {str(e)}")
        return jsonify({'error': 'Calculation failed'}), 500

@app.route('/api/send_orders', methods=['POST'])
@require_auth
def send_orders():
    """Send orders to MT5"""
    try:
        if not request.account_id:
            return jsonify({'error': 'Account not connected'}), 400
        
        data = request.json
        
        # This would implement actual MT5 order sending
        # For now, return success response
        
        log_audit(request.user_id, 'orders_sent', 
                  f'Account: {request.account_id}', 
                  request.remote_addr)
        
        return jsonify({
            'message': 'Orders sent successfully',
            'account_id': request.account_id,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Send orders error: {str(e)}")
        return jsonify({'error': 'Failed to send orders'}), 500

@app.route('/api/broadcast_orders', methods=['POST'])
@require_auth
@require_role('super_admin')
def broadcast_orders():
    """Broadcast orders to all users with broadcast role"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['symbol', 'entryPrice1', 'stopLoss', 'riskPercent']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields for broadcast'}), 400
        
        # Get all users with broadcast role
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username FROM users 
            WHERE role = 'broadcast' AND is_active = TRUE
        ''')
        broadcast_users = cursor.fetchall()
        
        if not broadcast_users:
            return jsonify({'error': 'No broadcast users found'}), 404
        
        # Add orders to broadcast queue for each user
        broadcast_count = 0
        order_data_json = str(data)  # Convert to JSON string for storage
        
        for user_id, username in broadcast_users:
            cursor.execute('''
                INSERT INTO broadcast_queue 
                (admin_user_id, target_user_id, order_data, status)
                VALUES (?, ?, ?, 'pending')
            ''', (request.user_id, user_id, order_data_json))
            broadcast_count += 1
        
        conn.commit()
        conn.close()
        
        # Log the broadcast action
        log_audit(request.user_id, 'broadcast_sent', 
                  f'Broadcast to {broadcast_count} users: {data.get("symbol", "")}', 
                  request.remote_addr)
        
        # Process broadcast queue (execute orders for all users)
        success_count = process_broadcast_queue()
        
        return jsonify({
            'message': 'Broadcast orders sent successfully',
            'target_users': broadcast_count,
            'executed_successfully': success_count,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Broadcast orders error: {str(e)}")
        return jsonify({'error': 'Failed to broadcast orders'}), 500

def process_broadcast_queue():
    """Process pending broadcast orders"""
    success_count = 0
    
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Get pending broadcast orders
        cursor.execute('''
            SELECT bq.id, bq.target_user_id, bq.order_data, u.username
            FROM broadcast_queue bq
            JOIN users u ON bq.target_user_id = u.id
            WHERE bq.status = 'pending'
            ORDER BY bq.created_at
        ''')
        
        pending_orders = cursor.fetchall()
        
        for order_id, user_id, order_data_json, username in pending_orders:
            try:
                # Parse order data
                import json
                order_data = eval(order_data_json)  # Convert string back to dict
                
                # Get user's active MT5 accounts
                cursor.execute('''
                    SELECT id, login, password_encrypted, server, account_name
                    FROM mt5_accounts 
                    WHERE user_id = ? AND is_active = TRUE
                    LIMIT 1
                ''', (user_id,))
                
                account = cursor.fetchone()
                
                if account:
                    account_id, login, password_encrypted, server, account_name = account
                    
                    # Calculate lot size for this user's portfolio
                    # For broadcast, use default portfolio size or get from user's last calculation
                    portfolio_size = order_data.get('portfolioSize', 1000)
                    risk_percent = order_data.get('riskPercent', 2)
                    entry_price = float(order_data['entryPrice1'])
                    stop_loss = float(order_data['stopLoss'])
                    
                    risk_amount = portfolio_size * (risk_percent / 100)
                    stop_distance = abs(entry_price - stop_loss)
                    contract_size = 100  # oz per lot for Gold
                    lot_size = risk_amount / (contract_size * stop_distance)
                    
                    # Here you would implement actual MT5 order sending
                    # For now, we'll mark as executed
                    
                    # Update broadcast queue status
                    cursor.execute('''
                        UPDATE broadcast_queue 
                        SET status = 'executed', executed_at = ?
                        WHERE id = ?
                    ''', (datetime.now(), order_id))
                    
                    success_count += 1
                    
                    # Log individual execution
                    log_audit(user_id, 'broadcast_order_executed', 
                             f'Symbol: {order_data["symbol"]}, Lot: {lot_size:.4f}', 
                             None)
                    
                    logger.info(f"Broadcast order executed for user {username} (ID: {user_id})")
                    
                else:
                    # No active MT5 account found
                    cursor.execute('''
                        UPDATE broadcast_queue 
                        SET status = 'failed', error_message = 'No active MT5 account'
                        WHERE id = ?
                    ''', (order_id,))
                    
                    logger.warning(f"No active MT5 account for broadcast user {username} (ID: {user_id})")
                    
            except Exception as order_error:
                # Mark individual order as failed
                cursor.execute('''
                    UPDATE broadcast_queue 
                    SET status = 'failed', error_message = ?
                    WHERE id = ?
                ''', (str(order_error), order_id))
                
                logger.error(f"Failed to execute broadcast order for user {username}: {str(order_error)}")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error processing broadcast queue: {str(e)}")
    
    return success_count

@app.route('/api/broadcast_status', methods=['GET'])
@require_auth
@require_role('super_admin')
def get_broadcast_status():
    """Get broadcast queue status"""
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # Get recent broadcast statistics
        cursor.execute('''
            SELECT 
                bq.status,
                COUNT(*) as count,
                MAX(bq.created_at) as latest_broadcast
            FROM broadcast_queue bq
            WHERE bq.admin_user_id = ?
            AND bq.created_at > datetime('now', '-24 hours')
            GROUP BY bq.status
        ''', (request.user_id,))
        
        status_stats = cursor.fetchall()
        
        # Get list of broadcast users
        cursor.execute('''
            SELECT id, username, last_login, is_active
            FROM users 
            WHERE role = 'broadcast'
            ORDER BY username
        ''')
        
        broadcast_users = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            'broadcast_statistics': [
                {
                    'status': row[0],
                    'count': row[1],
                    'latest': row[2]
                } for row in status_stats
            ],
            'broadcast_users': [
                {
                    'id': row[0],
                    'username': row[1],
                    'last_login': row[2],
                    'is_active': row[3]
                } for row in broadcast_users
            ],
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Get broadcast status error: {str(e)}")
        return jsonify({'error': 'Failed to get broadcast status'}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get server status"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'mt5_available': mt5 is not None,
        'active_connections': len(mt5_manager.connections),
        'version': '1.1.0'  # Updated version with broadcast feature
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Start server
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Multi-Account MT5 Trading Server on port {port}")
    logger.info(f"CORS origins: {Config.CORS_ORIGINS}")
    logger.info(f"Database: {Config.DATABASE_PATH}")
    
    # Support Railway.app and other cloud platforms
    port = int(os.environ.get('PORT', port))
    app.run(host='0.0.0.0', port=port, debug=debug)
