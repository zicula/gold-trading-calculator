#!/usr/bin/env python3
"""
MT5 Integration Server for Gold Trading Calculator
Local HTTP server to bridge web interface with MetaTrader 5

Author: Zic
Version: 1.0.0
"""

import json
import time
import logging
import platform
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# MT5 import with fallback for non-Windows systems
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
    print("✅ MetaTrader5 library loaded successfully")
except ImportError:
    print("⚠️  MetaTrader5 library not available (normal for macOS/Linux)")
    print("🔧 Using mock implementation for development")
    MT5_AVAILABLE = False
    
    # Mock MT5 implementation for development
    class MockMT5:
        @staticmethod
        def initialize():
            return True
            
        @staticmethod
        def account_info():
            return type('AccountInfo', (), {
                'login': 12345678,
                'trade_mode': 0,
                'leverage': 100,
                'limit_orders': 200,
                'margin_so_mode': 0,
                'trade_allowed': True,
                'trade_expert': True,
                'margin_mode': 0,
                'currency_digits': 2,
                'fifo_close': False,
                'balance': 10000.0,
                'credit': 0.0,
                'profit': 150.75,
                'equity': 10150.75,
                'margin': 500.0,
                'margin_free': 9650.75,
                'margin_level': 2030.15,
                'margin_so_call': 50.0,
                'margin_so_so': 30.0,
                'margin_initial': 0.0,
                'margin_maintenance': 0.0,
                'assets': 0.0,
                'liabilities': 0.0,
                'commission_blocked': 0.0,
                'name': "Demo Account",
                'server': "ConnextFX-Demo",
                'currency': "USD",
                'company': "ConnextFX Global"
            })()
        
        @staticmethod
        def symbol_info(symbol):
            return type('SymbolInfo', (), {
                'custom': False,
                'chart_mode': 0,
                'select': True,
                'visible': True,
                'session_deals': 0,
                'session_buy_orders': 0,
                'session_sell_orders': 0,
                'volume': 0,
                'volumehigh': 0,
                'volumelow': 0,
                'time': 1692105600,
                'digits': 3,
                'spread': 25,
                'spread_float': True,
                'ticks_bookdepth': 1,
                'trade_calc_mode': 0,
                'trade_mode': 4,
                'start_time': 0,
                'expiration_time': 0,
                'trade_stops_level': 0,
                'trade_freeze_level': 0,
                'trade_exemode': 1,
                'swap_mode': 1,
                'swap_rollover3days': 3,
                'margin_hedged_use_leg': False,
                'expiration_mode': 7,
                'filling_mode': 1,
                'order_mode': 127,
                'order_gtc_mode': 0,
                'option_mode': 0,
                'option_right': 0,
                'bid': 2650.123,
                'bidhigh': 2655.789,
                'bidlow': 2645.456,
                'ask': 2650.148,
                'askhigh': 2655.814,
                'asklow': 2645.481,
                'last': 2650.135,
                'lasthigh': 2655.801,
                'lastlow': 2645.468,
                'volume_real': 0.0,
                'volumehigh_real': 0.0,
                'volumelow_real': 0.0,
                'option_strike': 0.0,
                'point': 0.001,
                'trade_tick_value': 0.1,
                'trade_tick_value_profit': 0.1,
                'trade_tick_value_loss': 0.1,
                'trade_tick_size': 0.001,
                'trade_contract_size': 100.0,
                'trade_accrued_interest': 0.0,
                'trade_face_value': 0.0,
                'trade_liquidity_rate': 0.0,
                'volume_min': 0.01,
                'volume_max': 500.0,
                'volume_step': 0.01,
                'volume_limit': 0.0,
                'swap_long': -12.34,
                'swap_short': -5.67,
                'margin_initial': 0.0,
                'margin_maintenance': 0.0,
                'session_volume': 0.0,
                'session_turnover': 0.0,
                'session_interest': 0.0,
                'session_buy_orders_volume': 0.0,
                'session_sell_orders_volume': 0.0,
                'session_open': 2648.789,
                'session_close': 2650.135,
                'session_aw': 0.0,
                'session_price_settlement': 0.0,
                'session_price_limit_min': 0.0,
                'session_price_limit_max': 0.0,
                'margin_hedged': 0.0,
                'price_change': 1.346,
                'price_volatility': 0.0,
                'price_theoretical': 0.0,
                'price_greeks_delta': 0.0,
                'price_greeks_theta': 0.0,
                'price_greeks_gamma': 0.0,
                'price_greeks_vega': 0.0,
                'price_greeks_rho': 0.0,
                'price_greeks_omega': 0.0,
                'price_sensitivity': 0.0,
                'basis': "",
                'category': "",
                'currency_base': "XAU",
                'currency_profit': "USD",
                'currency_margin': "USD",
                'bank': "",
                'description': "Gold vs US Dollar",
                'exchange': "",
                'formula': "",
                'isin': "",
                'name': "XAUUSD",
                'page': "",
                'path': "Forex\\Metals"
            })()
        
        @staticmethod
        def order_send(request):
            # Mock successful order response
            return type('TradeResult', (), {
                'retcode': 10009,  # TRADE_RETCODE_DONE
                'deal': 123456789,
                'order': 987654321,
                'volume': request.get('volume', 0.01),
                'price': request.get('price', 2650.123),
                'bid': 2650.123,
                'ask': 2650.148,
                'comment': "Mock order placed successfully",
                'request_id': 1,
                'retcode_external': 0
            })()
        
        @staticmethod
        def shutdown():
            return True
            
        # Trade request constants
        TRADE_ACTION_DEAL = 1
        TRADE_ACTION_PENDING = 5
        ORDER_TYPE_BUY = 0
        ORDER_TYPE_SELL = 1
        ORDER_TYPE_BUY_LIMIT = 2
        ORDER_TYPE_SELL_LIMIT = 3
        ORDER_TYPE_BUY_STOP = 4
        ORDER_TYPE_SELL_STOP = 5
        ORDER_FILLING_IOC = 1
        ORDER_TIME_GTC = 0
    
    mt5 = MockMT5()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mt5_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for web requests

class MT5Bridge:
    """Bridge class to handle MT5 connections and operations"""
    
    def __init__(self):
        self.is_connected = False
        self.account_info = None
        
    def connect(self):
        """Initialize connection to MT5"""
        try:
            if not mt5.initialize():
                logger.error("Failed to initialize MT5")
                return False
                
            self.account_info = mt5.account_info()
            if self.account_info is None:
                logger.error("Failed to get account info")
                return False
                
            self.is_connected = True
            logger.info(f"Connected to MT5 account: {self.account_info.login}")
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to MT5: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MT5"""
        mt5.shutdown()
        self.is_connected = False
        self.account_info = None
        logger.info("Disconnected from MT5")
    
    def get_status(self):
        """Get connection status and account info"""
        if not self.is_connected:
            # Try to reconnect
            self.connect()
            
        return {
            'mt5_connected': self.is_connected,
            'account_info': {
                'login': self.account_info.login if self.account_info else None,
                'server': self.account_info.server if self.account_info else None,
                'balance': self.account_info.balance if self.account_info else None,
                'equity': self.account_info.equity if self.account_info else None,
                'margin': self.account_info.margin if self.account_info else None,
            } if self.account_info else None
        }
    
    def get_symbol_info(self, symbol="XAUUSD"):
        """Get symbol information and current price"""
        if not self.is_connected:
            return None
            
        try:
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                logger.error(f"Symbol {symbol} not found")
                return None
                
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                logger.error(f"Failed to get tick for {symbol}")
                return None
                
            return {
                'symbol': symbol,
                'bid': tick.bid,
                'ask': tick.ask,
                'spread': tick.ask - tick.bid,
                'point': symbol_info.point,
                'digits': symbol_info.digits,
                'trade_mode': symbol_info.trade_mode
            }
            
        except Exception as e:
            logger.error(f"Error getting symbol info: {e}")
            return None
    
    def send_market_order(self, symbol, order_type, volume, sl=None, tp=None, comment=""):
        """Send market order to MT5"""
        if not self.is_connected:
            return {'success': False, 'error': 'Not connected to MT5'}
            
        try:
            # Get current price
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                return {'success': False, 'error': f'Cannot get price for {symbol}'}
            
            price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
            
            # Prepare request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "deviation": 20,
                "magic": 12345,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Add SL/TP if provided
            if sl is not None:
                request["sl"] = sl
            if tp is not None:
                request["tp"] = tp
            
            # Send order
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                error_msg = f"Order failed: {result.retcode} - {result.comment}"
                logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            logger.info(f"Order sent successfully: {result.order}")
            return {
                'success': True,
                'order_id': result.order,
                'volume': result.volume,
                'price': result.price
            }
            
        except Exception as e:
            error_msg = f"Error sending order: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def send_pending_order(self, symbol, order_type, volume, price, sl=None, tp=None, comment=""):
        """Send pending order to MT5"""
        if not self.is_connected:
            return {'success': False, 'error': 'Not connected to MT5'}
            
        try:
            # Prepare request
            request = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "price": price,
                "deviation": 20,
                "magic": 12345,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_RETURN,
            }
            
            # Add SL/TP if provided
            if sl is not None:
                request["sl"] = sl
            if tp is not None:
                request["tp"] = tp
            
            # Send order
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                error_msg = f"Pending order failed: {result.retcode} - {result.comment}"
                logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            logger.info(f"Pending order sent successfully: {result.order}")
            return {
                'success': True,
                'order_id': result.order,
                'volume': result.volume,
                'price': result.price
            }
            
        except Exception as e:
            error_msg = f"Error sending pending order: {e}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}

# Initialize MT5 bridge
mt5_bridge = MT5Bridge()

@app.route('/status', methods=['GET'])
def get_status():
    """Get server and MT5 status"""
    try:
        status = mt5_bridge.get_status()
        return jsonify({
            'server_status': 'running',
            'timestamp': datetime.now().isoformat(),
            **status
        })
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/symbol_info', methods=['GET'])
def get_symbol_info():
    """Get symbol information"""
    symbol = request.args.get('symbol', 'XAUUSD')
    try:
        info = mt5_bridge.get_symbol_info(symbol)
        if info:
            return jsonify(info)
        else:
            return jsonify({'error': f'Symbol {symbol} not found'}), 404
    except Exception as e:
        logger.error(f"Error getting symbol info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/send_orders', methods=['POST'])
def send_orders():
    """Send orders to MT5 based on calculator data"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        logger.info(f"Received order data: {json.dumps(data, indent=2)}")
        
        # Validate required fields
        required_fields = ['direction', 'stopLoss', 'totalLotSize']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        symbol = data.get('symbol', 'XAUUSD')
        direction = data['direction'].lower()
        stop_loss = float(data['stopLoss'])
        total_lot_size = float(data['totalLotSize'])
        
        # Determine order type
        order_type = mt5.ORDER_TYPE_BUY if direction == 'buy' else mt5.ORDER_TYPE_SELL
        
        orders_sent = []
        
        # Check if we have zone breakdown
        if 'orderBreakdown' in data and data['orderBreakdown']:
            # Multi-zone orders
            zone1 = data['orderBreakdown']['zone1']
            zone2 = data['orderBreakdown']['zone2']
            
            # Send orders for each zone
            zones = [
                {'price': zone1['price'], 'lot': zone1['lot'], 'zone': 1},
                {'price': zone2['price'], 'lot': zone2['lot'], 'zone': 2}
            ]
            
            for zone in zones:
                # Determine if this should be a market or pending order
                # For simplicity, we'll use pending orders for specific prices
                pending_order_type = (mt5.ORDER_TYPE_BUY_LIMIT if direction == 'buy' 
                                    else mt5.ORDER_TYPE_SELL_LIMIT)
                
                comment = f"Auto Trade Zone {zone['zone']} - Calculator"
                
                result = mt5_bridge.send_pending_order(
                    symbol=symbol,
                    order_type=pending_order_type,
                    volume=zone['lot'],
                    price=zone['price'],
                    sl=stop_loss,
                    tp=None,  # Will set TP separately
                    comment=comment
                )
                
                if result['success']:
                    orders_sent.append({
                        'zone': zone['zone'],
                        'order_id': result['order_id'],
                        'price': zone['price'],
                        'volume': zone['lot']
                    })
                else:
                    logger.error(f"Failed to send order for zone {zone['zone']}: {result['error']}")
        
        else:
            # Single order
            entry_price = data.get('entryPrice1') or data.get('avgEntryPrice')
            
            if entry_price:
                # Pending order at specific price
                pending_order_type = (mt5.ORDER_TYPE_BUY_LIMIT if direction == 'buy' 
                                    else mt5.ORDER_TYPE_SELL_LIMIT)
                
                result = mt5_bridge.send_pending_order(
                    symbol=symbol,
                    order_type=pending_order_type,
                    volume=total_lot_size,
                    price=entry_price,
                    sl=stop_loss,
                    tp=None,
                    comment="Auto Trade - Calculator"
                )
            else:
                # Market order
                result = mt5_bridge.send_market_order(
                    symbol=symbol,
                    order_type=order_type,
                    volume=total_lot_size,
                    sl=stop_loss,
                    tp=None,
                    comment="Auto Trade - Calculator"
                )
            
            if result['success']:
                orders_sent.append({
                    'order_id': result['order_id'],
                    'volume': result['volume'],
                    'price': result.get('price', entry_price)
                })
        
        # Handle TP levels (if any)
        tp_orders = []
        if 'tpLevels' in data and data['tpLevels']:
            # For now, just log TP levels - implementing TP modification requires position management
            logger.info(f"TP Levels to be set: {[tp['price'] for tp in data['tpLevels']]}")
        
        return jsonify({
            'success': True,
            'orders_sent': len(orders_sent),
            'orders': orders_sent,
            'tp_levels': tp_orders,
            'message': f'Successfully sent {len(orders_sent)} orders to MT5'
        })
        
    except Exception as e:
        error_msg = f"Error processing orders: {e}"
        logger.error(error_msg)
        return jsonify({'success': False, 'error': error_msg}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting MT5 Integration Server...")
    print("📊 Gold Trading Calculator - Local Server")
    print("🔗 Server will run on: http://localhost:8080")
    print("⚠️  Make sure MT5 is running and Auto Trading is enabled")
    print("-" * 50)
    
    # Try to connect to MT5 on startup
    if mt5_bridge.connect():
        print("✅ MT5 connection successful")
    else:
        print("❌ MT5 connection failed - will retry when needed")
    
    print("-" * 50)
    print("🌐 Server starting...")
    
    # Run Flask app
    app.run(
        host='localhost',
        port=8080,
        debug=False,  # Set to True for development
        threaded=True
    )
