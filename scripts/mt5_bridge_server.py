#!/usr/bin/env python3
"""
MT5 Bridge Server for Windows VPS/PC
เชื่อมต่อ MetaTrader 5 กับ Web Application บน Ubuntu VPS

Requirements:
- Windows OS with MetaTrader 5 installed
- pip install MetaTrader5 flask flask-cors python-dotenv

Usage:
python scripts/mt5_bridge_server.py
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

# Try to import MetaTrader5
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    print("❌ MetaTrader5 library not found!")
    print("📥 Install with: pip install MetaTrader5")
    print("⚠️  Note: MetaTrader5 works only on Windows!")
    MT5_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mt5_bridge.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Global variables
connected_accounts = {}
API_KEY = os.getenv('MT5_BRIDGE_API_KEY', 'your-secret-api-key-here')

def require_api_key(f):
    """Decorator for API key authentication"""
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if api_key != API_KEY:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'mt5_available': MT5_AVAILABLE,
        'timestamp': datetime.now().isoformat(),
        'connected_accounts': len(connected_accounts)
    })

@app.route('/mt5/status', methods=['GET'])
@require_api_key
def mt5_status():
    """Check MT5 status and connected accounts"""
    if not MT5_AVAILABLE:
        return jsonify({'error': 'MT5 not available on this system'}), 400
    
    try:
        # Check if MT5 is initialized
        if not mt5.initialize():
            return jsonify({
                'status': 'disconnected',
                'message': 'MT5 terminal not initialized',
                'connected_accounts': len(connected_accounts)
            })
        
        # Get terminal info
        terminal_info = mt5.terminal_info()
        version_info = mt5.version()
        
        return jsonify({
            'status': 'connected',
            'terminal_info': {
                'build': terminal_info.build if terminal_info else None,
                'name': terminal_info.name if terminal_info else None,
                'path': terminal_info.path if terminal_info else None
            },
            'version': {
                'version': version_info[0] if version_info else None,
                'build': version_info[1] if version_info else None,
                'date': version_info[2] if version_info else None
            },
            'connected_accounts': len(connected_accounts)
        })
        
    except Exception as e:
        logger.error(f"Error checking MT5 status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/mt5/connect', methods=['POST'])
@require_api_key
def connect_mt5():
    """Connect to MT5 account"""
    if not MT5_AVAILABLE:
        return jsonify({'error': 'MT5 not available on this system'}), 400
    
    try:
        data = request.json
        login = data.get('login')
        password = data.get('password')
        server = data.get('server')
        account_name = data.get('account_name', f'Account_{login}')
        
        if not all([login, password, server]):
            return jsonify({'error': 'Missing login, password, or server'}), 400
        
        # Initialize MT5
        if not mt5.initialize():
            return jsonify({'error': 'Failed to initialize MT5 terminal'}), 500
        
        # Login to account
        authorized = mt5.login(login, password=password, server=server)
        
        if authorized:
            # Get account info
            account_info = mt5.account_info()
            if account_info:
                # Store connection info
                connected_accounts[str(login)] = {
                    'login': login,
                    'server': server,
                    'account_name': account_name,
                    'connected_at': datetime.now().isoformat(),
                    'account_info': {
                        'balance': account_info.balance,
                        'equity': account_info.equity,
                        'margin': account_info.margin,
                        'currency': account_info.currency,
                        'leverage': account_info.leverage,
                        'profit': account_info.profit
                    }
                }
                
                logger.info(f"Successfully connected to MT5 account: {login} on {server}")
                return jsonify({
                    'status': 'connected',
                    'account_name': account_name,
                    'login': login,
                    'server': server,
                    'account_info': connected_accounts[str(login)]['account_info']
                })
            else:
                return jsonify({'error': 'Failed to get account info after login'}), 500
        else:
            error_code = mt5.last_error()
            logger.error(f"Failed to connect to MT5: {error_code}")
            return jsonify({
                'error': f'Failed to login to MT5 account',
                'details': f'Error code: {error_code}'
            }), 400
            
    except Exception as e:
        logger.error(f"Error connecting to MT5: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/mt5/account_info/<account_login>', methods=['GET'])
@require_api_key
def get_account_info(account_login):
    """Get account information"""
    if not MT5_AVAILABLE:
        return jsonify({'error': 'MT5 not available on this system'}), 400
    
    try:
        # Check if account is connected
        if account_login not in connected_accounts:
            return jsonify({'error': f'Account {account_login} not connected'}), 404
        
        # Switch to the account and get fresh info
        account = connected_accounts[account_login]
        authorized = mt5.login(account['login'], server=account['server'])
        
        if not authorized:
            return jsonify({'error': 'Failed to switch to account'}), 500
        
        account_info = mt5.account_info()
        if account_info:
            # Update stored info
            connected_accounts[account_login]['account_info'] = {
                'balance': account_info.balance,
                'equity': account_info.equity,
                'margin': account_info.margin,
                'currency': account_info.currency,
                'leverage': account_info.leverage,
                'profit': account_info.profit,
                'margin_free': account_info.margin_free,
                'margin_level': account_info.margin_level
            }
            
            return jsonify({
                'status': 'success',
                'account_name': account['account_name'],
                'account_info': connected_accounts[account_login]['account_info']
            })
        else:
            return jsonify({'error': 'Failed to get account info'}), 500
            
    except Exception as e:
        logger.error(f"Error getting account info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/mt5/positions/<account_login>', methods=['GET'])
@require_api_key
def get_positions(account_login):
    """Get open positions for account"""
    if not MT5_AVAILABLE:
        return jsonify({'error': 'MT5 not available on this system'}), 400
    
    try:
        # Check if account is connected
        if account_login not in connected_accounts:
            return jsonify({'error': f'Account {account_login} not connected'}), 404
        
        # Switch to the account
        account = connected_accounts[account_login]
        authorized = mt5.login(account['login'], server=account['server'])
        
        if not authorized:
            return jsonify({'error': 'Failed to switch to account'}), 500
        
        # Get positions
        positions = mt5.positions_get()
        
        if positions is None:
            positions = []
        
        positions_list = []
        for pos in positions:
            positions_list.append({
                'ticket': pos.ticket,
                'symbol': pos.symbol,
                'type': pos.type,
                'volume': pos.volume,
                'price_open': pos.price_open,
                'price_current': pos.price_current,
                'profit': pos.profit,
                'swap': pos.swap,
                'time': pos.time
            })
        
        return jsonify({
            'status': 'success',
            'account_name': account['account_name'],
            'positions': positions_list,
            'total_positions': len(positions_list)
        })
        
    except Exception as e:
        logger.error(f"Error getting positions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/mt5/symbols/<account_login>', methods=['GET'])
@require_api_key
def get_symbols(account_login):
    """Get available symbols for account"""
    if not MT5_AVAILABLE:
        return jsonify({'error': 'MT5 not available on this system'}), 400
    
    try:
        # Check if account is connected
        if account_login not in connected_accounts:
            return jsonify({'error': f'Account {account_login} not connected'}), 404
        
        # Switch to the account
        account = connected_accounts[account_login]
        authorized = mt5.login(account['login'], server=account['server'])
        
        if not authorized:
            return jsonify({'error': 'Failed to switch to account'}), 500
        
        # Get symbols
        symbols = mt5.symbols_get()
        
        if symbols is None:
            symbols = []
        
        symbols_list = []
        for symbol in symbols:
            if 'GOLD' in symbol.name or 'XAUUSD' in symbol.name:
                symbols_list.append({
                    'name': symbol.name,
                    'description': symbol.description,
                    'digits': symbol.digits,
                    'spread': symbol.spread,
                    'volume_min': symbol.volume_min,
                    'volume_max': symbol.volume_max,
                    'volume_step': symbol.volume_step
                })
        
        return jsonify({
            'status': 'success',
            'account_name': account['account_name'],
            'symbols': symbols_list,
            'total_symbols': len(symbols_list)
        })
        
    except Exception as e:
        logger.error(f"Error getting symbols: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/mt5/disconnect/<account_login>', methods=['POST'])
@require_api_key
def disconnect_account(account_login):
    """Disconnect from MT5 account"""
    try:
        if account_login in connected_accounts:
            del connected_accounts[account_login]
            logger.info(f"Disconnected from MT5 account: {account_login}")
            return jsonify({'status': 'disconnected', 'account_login': account_login})
        else:
            return jsonify({'error': f'Account {account_login} not found'}), 404
            
    except Exception as e:
        logger.error(f"Error disconnecting account: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/mt5/accounts', methods=['GET'])
@require_api_key
def list_connected_accounts():
    """List all connected accounts"""
    try:
        accounts = []
        for login, account in connected_accounts.items():
            accounts.append({
                'login': login,
                'account_name': account['account_name'],
                'server': account['server'],
                'connected_at': account['connected_at'],
                'balance': account['account_info'].get('balance', 0),
                'equity': account['account_info'].get('equity', 0),
                'currency': account['account_info'].get('currency', 'USD')
            })
        
        return jsonify({
            'status': 'success',
            'accounts': accounts,
            'total_accounts': len(accounts)
        })
        
    except Exception as e:
        logger.error(f"Error listing accounts: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not MT5_AVAILABLE:
        print("\n❌ MetaTrader5 library not available!")
        print("This script must be run on Windows with MetaTrader5 installed.")
        print("Install the library with: pip install MetaTrader5")
        sys.exit(1)
    
    print("\n🚀 Starting MT5 Bridge Server...")
    print(f"📡 Server will run on: http://0.0.0.0:8081")
    print(f"🔑 API Key: {API_KEY}")
    print("📋 Endpoints:")
    print("  GET  /health                         - Health check")
    print("  GET  /mt5/status                     - MT5 status")
    print("  POST /mt5/connect                    - Connect account")
    print("  GET  /mt5/account_info/<login>       - Account info")
    print("  GET  /mt5/positions/<login>          - Get positions")
    print("  GET  /mt5/symbols/<login>            - Get symbols")
    print("  POST /mt5/disconnect/<login>         - Disconnect account")
    print("  GET  /mt5/accounts                   - List all accounts")
    print("\n💡 All endpoints require X-API-Key header or api_key parameter")
    print("🔧 Make sure MetaTrader 5 is running and Auto Trading is enabled")
    print("\n" + "="*60)
    
    try:
        app.run(host='0.0.0.0', port=8081, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Shutting down MT5 Bridge Server...")
        if MT5_AVAILABLE:
            mt5.shutdown()
        sys.exit(0)
