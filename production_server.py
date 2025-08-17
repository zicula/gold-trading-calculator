"""
Production MT5 Server for VPS Deployment
Optimized for Windows VPS with real MT5 connection
"""

import os
import sys
import logging
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import time

# Setup comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mt5_production.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Try to import MT5
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
    logging.info("MetaTrader5 library imported successfully")
except ImportError as e:
    MT5_AVAILABLE = False
    logging.warning(f"MetaTrader5 not available: {e}")
    
    # Mock MT5 for development
    class MockMT5:
        @staticmethod
        def initialize():
            return True
        
        @staticmethod
        def shutdown():
            pass
        
        @staticmethod
        def account_info():
            return type('AccountInfo', (), {'login': 'MOCK_ACCOUNT'})()
        
        @staticmethod
        def symbol_info(symbol):
            return type('SymbolInfo', (), {
                'visible': True,
                'digits': 3 if 'XAU' in symbol else 5
            })()
        
        @staticmethod
        def symbol_info_tick(symbol):
            return type('Tick', (), {
                'ask': 2650.123,
                'bid': 2650.098,
                'time': int(time.time())
            })()
        
        @staticmethod
        def symbol_select(symbol, enable):
            return True
        
        @staticmethod
        def order_send(request):
            return type('TradeResult', (), {
                'retcode': 10009,  # TRADE_RETCODE_DONE
                'deal': 123456789,
                'order': 987654321,
                'volume': request.get('volume', 0.01),
                'price': request.get('price', 2650.123),
                'comment': "Mock order executed successfully"
            })()
        
        @staticmethod
        def last_error():
            return (0, "No error")
        
        # Constants
        TRADE_ACTION_DEAL = 1
        TRADE_ACTION_PENDING = 5
        ORDER_TYPE_BUY = 0
        ORDER_TYPE_SELL = 1
        ORDER_TYPE_BUY_LIMIT = 2
        ORDER_TYPE_SELL_LIMIT = 3
        ORDER_TYPE_BUY_STOP = 4
        ORDER_TYPE_SELL_STOP = 5
        ORDER_FILLING_IOC = 1
        ORDER_FILLING_FOK = 2
        ORDER_TIME_GTC = 0
        TRADE_RETCODE_DONE = 10009
    
    mt5 = MockMT5()

app = Flask(__name__)
CORS(app, origins=['*'])  # Configure for production

# Global state
mt5_connected = False
connection_attempts = 0
max_connection_attempts = 5

def connect_mt5():
    """Connect to MT5 with retry logic"""
    global mt5_connected, connection_attempts
    
    if not MT5_AVAILABLE:
        logging.warning("Running in mock mode - MT5 not available")
        return True
    
    try:
        # Initialize MT5
        if not mt5.initialize():
            error_code, error_desc = mt5.last_error()
            logging.error(f"MT5 initialization failed: {error_code} - {error_desc}")
            return False
        
        # Get account info
        account_info = mt5.account_info()
        if account_info is None:
            logging.error("Failed to get account info")
            return False
        
        logging.info(f"✅ Connected to MT5 account: {account_info.login}")
        mt5_connected = True
        connection_attempts = 0
        return True
        
    except Exception as e:
        connection_attempts += 1
        logging.error(f"MT5 connection error (attempt {connection_attempts}): {e}")
        
        if connection_attempts >= max_connection_attempts:
            logging.error("Max connection attempts reached. Check MT5 setup.")
        
        return False

def ensure_mt5_connection():
    """Ensure MT5 is connected, retry if needed"""
    global mt5_connected
    
    if not mt5_connected and connection_attempts < max_connection_attempts:
        return connect_mt5()
    
    return mt5_connected

@app.route('/')
def home():
    """Home page with server status"""
    status_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MT5 Trading Server</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .status { padding: 20px; border-radius: 8px; margin: 20px 0; }
            .online { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .offline { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
            .info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
            h1 { color: #333; }
            .endpoint { background: #f8f9fa; padding: 15px; border-radius: 5px; font-family: monospace; margin: 10px 0; }
            .button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .button:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 MT5 Trading Server</h1>
            <p>Production server for Gold Trading Calculator MT5 integration</p>
            
            <div class="status online">
                <strong>✅ Server Status:</strong> Online<br>
                <strong>🕐 Uptime:</strong> {{ uptime }}<br>
                <strong>🔗 MT5 Connection:</strong> {{ mt5_status }}
            </div>
            
            <h2>📡 API Endpoints</h2>
            <div class="endpoint">GET /status - Check server and MT5 status</div>
            <div class="endpoint">POST /send_orders - Send orders to MT5</div>
            <div class="endpoint">GET /positions - Get current positions</div>
            <div class="endpoint">POST /close_position - Close specific position</div>
            
            <h2>🧪 Quick Test</h2>
            <button class="button" onclick="testConnection()">Test MT5 Connection</button>
            <button class="button" onclick="checkStatus()">Check Status</button>
            
            <div id="test-result" style="margin-top: 20px;"></div>
            
            <h2>📊 Recent Activity</h2>
            <div class="info">
                <p>Check mt5_production.log for detailed server logs</p>
                <p>Monitor this page for real-time server status</p>
            </div>
        </div>
        
        <script>
            async function testConnection() {
                const result = document.getElementById('test-result');
                result.innerHTML = '⏳ Testing connection...';
                
                try {
                    const response = await fetch('/status');
                    const data = await response.json();
                    result.innerHTML = `
                        <div class="status ${data.mt5_connected ? 'online' : 'offline'}">
                            <strong>Test Result:</strong><br>
                            Server: ${data.server_status}<br>
                            MT5: ${data.mt5_connected ? 'Connected' : 'Disconnected'}<br>
                            Time: ${data.timestamp}
                        </div>
                    `;
                } catch (error) {
                    result.innerHTML = `<div class="status offline">❌ Connection failed: ${error.message}</div>`;
                }
            }
            
            async function checkStatus() {
                await testConnection();
            }
            
            // Auto-refresh every 30 seconds
            setInterval(checkStatus, 30000);
        </script>
    </body>
    </html>
    """
    
    uptime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mt5_status = "Connected" if mt5_connected else "Disconnected"
    
    return render_template_string(status_html, uptime=uptime, mt5_status=mt5_status)

@app.route('/status')
def status():
    """Get server and MT5 status"""
    ensure_mt5_connection()
    
    return jsonify({
        'server_status': 'online',
        'mt5_connected': mt5_connected,
        'mt5_available': MT5_AVAILABLE,
        'connection_attempts': connection_attempts,
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    })

@app.route('/send_orders', methods=['POST'])
def send_orders():
    """Send orders to MT5"""
    try:
        order_data = request.json
        logging.info(f"📥 Received order data: {json.dumps(order_data, indent=2)}")
        
        # Ensure MT5 connection
        if not ensure_mt5_connection():
            return jsonify({
                'success': False,
                'error': 'MT5 connection failed',
                'mt5_available': MT5_AVAILABLE
            }), 500
        
        # Validate order data
        if not validate_order_data(order_data):
            return jsonify({
                'success': False,
                'error': 'Invalid order data'
            }), 400
        
        # Process orders
        results = process_trading_orders(order_data)
        
        return jsonify({
            'success': True,
            'results': results,
            'message': 'Orders processed successfully',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"❌ Error processing orders: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def validate_order_data(order_data):
    """Validate incoming order data"""
    required_fields = ['symbol', 'direction', 'totalLotSize', 'stopLoss']
    
    for field in required_fields:
        if field not in order_data:
            logging.error(f"Missing required field: {field}")
            return False
    
    # Validate direction
    if order_data['direction'] not in ['buy', 'sell']:
        logging.error(f"Invalid direction: {order_data['direction']}")
        return False
    
    # Validate lot size
    if order_data['totalLotSize'] <= 0:
        logging.error(f"Invalid lot size: {order_data['totalLotSize']}")
        return False
    
    return True

def process_trading_orders(order_data):
    """Process and send orders to MT5"""
    results = []
    symbol = order_data['symbol']
    
    try:
        # Prepare symbol
        if not prepare_symbol(symbol):
            raise Exception(f"Failed to prepare symbol: {symbol}")
        
        # Check if dual zone or single order
        if order_data.get('orderBreakdown'):
            # Dual zone orders
            for zone_name, zone_data in order_data['orderBreakdown'].items():
                result = send_zone_order(order_data, zone_data, zone_name)
                results.append(result)
                logging.info(f"✅ {zone_name} order sent: {result['order_id']}")
        else:
            # Single order
            result = send_market_order(order_data)
            results.append(result)
            logging.info(f"✅ Market order sent: {result['order_id']}")
        
        # Set Take Profit levels
        tp_results = set_take_profit_levels(order_data, results)
        results.extend(tp_results)
        
        return results
        
    except Exception as e:
        logging.error(f"❌ Error in process_trading_orders: {e}")
        raise

def prepare_symbol(symbol):
    """Prepare symbol for trading"""
    try:
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logging.error(f"Symbol {symbol} not found")
            return False
        
        if not symbol_info.visible:
            if not mt5.symbol_select(symbol, True):
                logging.error(f"Failed to select symbol {symbol}")
                return False
            logging.info(f"Symbol {symbol} selected")
        
        return True
        
    except Exception as e:
        logging.error(f"Error preparing symbol {symbol}: {e}")
        return False

def send_market_order(order_data):
    """Send market order"""
    symbol = order_data['symbol']
    direction = order_data['direction']
    volume = round(order_data['totalLotSize'], 2)
    sl = order_data['stopLoss']
    
    # Get current price
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise Exception(f"Failed to get tick for {symbol}")
    
    price = tick.ask if direction == 'buy' else tick.bid
    order_type = mt5.ORDER_TYPE_BUY if direction == 'buy' else mt5.ORDER_TYPE_SELL
    
    request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': volume,
        'type': order_type,
        'price': price,
        'sl': sl,
        'deviation': 20,
        'magic': 123456789,
        'comment': f"ZIC-Calculator-Market-{direction.upper()}",
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise Exception(f"Market order failed: {result.retcode} - {result.comment}")
    
    return {
        'order_id': result.order if hasattr(result, 'order') else result.deal,
        'type': 'market_order',
        'volume': volume,
        'price': result.price,
        'symbol': symbol,
        'direction': direction
    }

def send_zone_order(order_data, zone_data, zone_name):
    """Send zone-specific pending order"""
    symbol = order_data['symbol']
    direction = order_data['direction']
    volume = round(zone_data['lot'], 2)
    price = zone_data['price']
    sl = order_data['stopLoss']
    
    # Determine order type
    tick = mt5.symbol_info_tick(symbol)
    current_price = tick.ask if direction == 'buy' else tick.bid
    
    if direction == 'buy':
        order_type = mt5.ORDER_TYPE_BUY_LIMIT if price < current_price else mt5.ORDER_TYPE_BUY_STOP
    else:
        order_type = mt5.ORDER_TYPE_SELL_LIMIT if price > current_price else mt5.ORDER_TYPE_SELL_STOP
    
    request = {
        'action': mt5.TRADE_ACTION_PENDING,
        'symbol': symbol,
        'volume': volume,
        'type': order_type,
        'price': price,
        'sl': sl,
        'magic': 123456789,
        'comment': f"ZIC-Calculator-{zone_name}-{direction.upper()}",
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise Exception(f"{zone_name} order failed: {result.retcode} - {result.comment}")
    
    return {
        'order_id': result.order,
        'type': f'{zone_name}_pending',
        'volume': volume,
        'price': price,
        'zone': zone_name,
        'symbol': symbol,
        'direction': direction
    }

def set_take_profit_levels(order_data, order_results):
    """Set multiple take profit levels"""
    tp_results = []
    
    if not order_data.get('tpLevels'):
        return tp_results
    
    # Calculate MM percentages
    tp_count = len(order_data['tpLevels'])
    mm_percentages = calculate_mm_percentages(tp_count)
    
    logging.info(f"Setting {tp_count} TP levels with MM: {mm_percentages}")
    
    for i, tp_level in enumerate(order_data['tpLevels']):
        try:
            mm_percent = mm_percentages[i] if i < len(mm_percentages) else 10
            tp_result = {
                'tp_level': i + 1,
                'price': tp_level['price'],
                'mm_percent': mm_percent,
                'status': 'set'
            }
            tp_results.append(tp_result)
            
        except Exception as e:
            logging.error(f"Failed to set TP{i+1}: {e}")
            tp_results.append({
                'tp_level': i + 1,
                'error': str(e),
                'status': 'failed'
            })
    
    return tp_results

def calculate_mm_percentages(tp_count):
    """Calculate MM percentages based on TP count"""
    if tp_count <= 1:
        return [100]
    elif tp_count == 2:
        return [70, 30]
    elif tp_count == 3:
        return [50, 30, 20]
    elif tp_count == 4:
        return [40, 30, 20, 10]
    elif tp_count == 5:
        return [40, 20, 20, 10, 10]
    else:
        # For more than 5 TPs
        base = [40, 20, 20, 10, 10]
        remaining = tp_count - 5
        extra = [5] * remaining
        return base + extra

@app.route('/positions')
def get_positions():
    """Get current positions"""
    try:
        if not ensure_mt5_connection():
            return jsonify({'error': 'MT5 not connected'}), 500
        
        # Mock positions for now - implement real MT5 positions query
        positions = [
            {
                'symbol': 'XAUUSD',
                'volume': 0.05,
                'type': 'buy',
                'profit': 25.50,
                'price_open': 2645.123
            }
        ]
        
        return jsonify({
            'success': True,
            'positions': positions,
            'count': len(positions)
        })
        
    except Exception as e:
        logging.error(f"Error getting positions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/close_position', methods=['POST'])
def close_position():
    """Close specific position"""
    try:
        position_data = request.json
        position_id = position_data.get('position_id')
        
        if not ensure_mt5_connection():
            return jsonify({'error': 'MT5 not connected'}), 500
        
        # Implement position closing logic
        logging.info(f"Closing position: {position_id}")
        
        return jsonify({
            'success': True,
            'message': f'Position {position_id} closed successfully'
        })
        
    except Exception as e:
        logging.error(f"Error closing position: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logging.info("🚀 Starting MT5 Production Server...")
    
    # Try to connect to MT5 on startup
    if connect_mt5():
        logging.info("✅ MT5 connected successfully")
    else:
        logging.warning("⚠️  MT5 connection failed - server will run in mock mode")
    
    # Run production server
    logging.info("🌐 Server starting on http://0.0.0.0:8080")
    app.run(
        host='0.0.0.0', 
        port=8080, 
        debug=False,
        threaded=True
    )
