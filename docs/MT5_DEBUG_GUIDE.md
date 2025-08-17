# 🔍 Multi-Account Calculator MT5 Backend Debug Guide

## 📋 Frontend → Backend Flow Analysis

### 🎯 การทำงานของ "ส่งคำสั่งไป MT5"

#### **1. Frontend JavaScript (multi_account_calculator.html)**

```javascript
async function sendToMT5() {
    // ตรวจสอบการเชื่อมต่อ account
    if (!currentAccount && !isBroadcastMode) {
        alert('กรุณาเชื่อมต่อบัญชี MT5 ก่อนส่งคำสั่ง');
        return;
    }
    
    // รวบรวมข้อมูลจากฟอร์ม
    const orderData = {
        symbol: document.getElementById('symbol').value,
        entryPrice1: document.getElementById('entryPrice1').value,
        stopLoss: document.getElementById('stopLoss').value,
        portfolioSize: document.getElementById('portfolioSize').value,
        riskPercent: document.getElementById('riskPercent').value
    };
    
    // ส่ง HTTP Request ไป Backend
    const response = await fetch(`${API_BASE}/send_orders`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(orderData)
    });
}
```

#### **2. Backend API Endpoint (backend/app.py)**

```python
@app.route('/api/send_orders', methods=['POST'])
@require_auth  # ตรวจสอบ JWT Token
def send_orders():
    """Send orders to MT5"""
    try:
        # ตรวจสอบว่ามี account เชื่อมต่อหรือไม่
        if not request.account_id:
            return jsonify({'error': 'Account not connected'}), 400
        
        data = request.json  # รับข้อมูลจาก Frontend
        
        # !! สำคัญ: ตรงนี้คือจุดที่ต้อง implement MT5 integration
        # ปัจจุบันเป็น mock response
        
        # Log การทำงาน
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
```

---

## 🔧 วิธี Debug แต่ละจุด

### **1. Debug Frontend (Browser)**

#### **Chrome DevTools:**
```javascript
// เปิด Developer Tools (F12) → Console
// ดูข้อมูลที่ส่งไป Backend:

console.log('Order Data:', orderData);
console.log('API URL:', `${API_BASE}/send_orders`);
console.log('Auth Token:', authToken);

// ดู Network Request:
// F12 → Network → กด "ส่งคำสั่งไป MT5" → ดู Request/Response
```

#### **Network Panel ใน DevTools:**
```
Method: POST
URL: /api/send_orders
Status: 200/400/500
Request Headers:
  - Authorization: Bearer JWT_TOKEN
  - Content-Type: application/json
Request Body:
  - symbol, entryPrice1, stopLoss, etc.
Response:
  - message/error
```

### **2. Debug Backend (Python)**

#### **เพิ่ม Debug Logs ใน backend/app.py:**
```python
@app.route('/api/send_orders', methods=['POST'])
@require_auth
def send_orders():
    try:
        # Debug: ดูข้อมูลที่เข้ามา
        logger.info(f"Send orders request from user: {request.user_id}")
        logger.info(f"Account ID: {request.account_id}")
        logger.info(f"Order data: {request.json}")
        
        data = request.json
        
        # Debug: ตรวจสอบข้อมูล
        logger.info(f"Symbol: {data.get('symbol')}")
        logger.info(f"Entry Price: {data.get('entryPrice1')}")
        logger.info(f"Stop Loss: {data.get('stopLoss')}")
        
        # !! จุดที่ต้อง implement MT5 integration
        mt5_result = send_to_real_mt5(data)  # ฟังก์ชันที่ต้องสร้าง
        
        return jsonify({
            'message': 'Orders sent successfully',
            'mt5_result': mt5_result,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Send orders error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500
```

### **3. Debug Log Files**

#### **ดู Log ใน Terminal:**
```bash
# ดู real-time logs
tail -f backend/logs/trading_server.log

# หรือ
tail -f mt5_production.log
```

#### **Log Format ที่จะเห็น:**
```
2024-08-17 20:15:30 - INFO - Send orders request from user: 1
2024-08-17 20:15:30 - INFO - Account ID: 123456
2024-08-17 20:15:30 - INFO - Order data: {'symbol': 'XAUUSD', 'entryPrice1': '2650'}
2024-08-17 20:15:30 - ERROR - MT5 connection failed: [Error details]
```

---

## ⚠️ ปัญหาที่พบบ่อย

### **1. Mock Mode (ไม่มี MT5 จริง)**
```python
# ใน Config class (backend/app.py)
MT5_MODE = os.getenv('MT5_MODE', 'mock')  # 'mock' หรือ 'production'

if MT5_MODE == 'mock':
    logger.info("Running in Mock Mode - MT5 commands simulated")
    return {'status': 'simulated', 'message': 'Order sent (mock)'}
```

### **2. Authentication Issues**
```javascript
// ตรวจสอบ Token
if (!authToken) {
    console.error('No auth token found');
    // ต้อง login ก่อน
}
```

### **3. CORS Issues**
```python
# ใน backend/app.py
CORS(app, origins=['*'])  # หรือระบุ domain เฉพาะ
```

---

## 🛠️ การ Implement MT5 Integration จริง

### **สร้างฟังก์ชัน MT5 จริง:**
```python
def send_to_real_mt5(order_data):
    """ส่งคำสั่งไป MT5 จริง"""
    try:
        if not MT5_AVAILABLE:
            return {'status': 'error', 'message': 'MT5 not available'}
        
        # เชื่อมต่อ MT5
        if not mt5.initialize():
            return {'status': 'error', 'message': 'MT5 initialization failed'}
        
        # ดึงข้อมูล account
        account_info = mt5.account_info()
        
        # สร้าง order request
        request_order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": order_data['symbol'],
            "volume": calculate_lot_size(order_data),
            "type": mt5.ORDER_TYPE_BUY,  # หรือ SELL
            "price": float(order_data['entryPrice1']),
            "sl": float(order_data['stopLoss']),
            "magic": 234000,
            "comment": "Gold Calculator Order",
        }
        
        # ส่ง order
        result = mt5.order_send(request_order)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return {
                'status': 'error', 
                'message': f'Order failed: {result.comment}',
                'retcode': result.retcode
            }
        
        return {
            'status': 'success',
            'ticket': result.order,
            'volume': result.volume,
            'price': result.price
        }
        
    except Exception as e:
        logger.error(f"MT5 order error: {str(e)}")
        return {'status': 'error', 'message': str(e)}
```

---

## 📊 Debug Checklist

### **✅ Frontend Debug:**
- [ ] Console.log ดูข้อมูลที่ส่ง
- [ ] Network panel ดู HTTP request/response
- [ ] ตรวจสอบ authToken และ API_BASE

### **✅ Backend Debug:**
- [ ] เพิ่ม logger.info() ในจุดสำคัญ
- [ ] ดู log files real-time
- [ ] ตรวจสอบ Exception handling

### **✅ MT5 Integration:**
- [ ] ตรวจสอบ MT5_MODE (mock/production)
- [ ] ทดสอบ MT5 connection
- [ ] Implement send_to_real_mt5() function

### **✅ Database:**
- [ ] ดู audit_logs table
- [ ] ตรวจสอบ account connection status
- [ ] ดู broadcast_queue table

---

**🎯 ขั้นตอนต่อไป:**
1. **เพิ่ม Debug Logs** ใน backend/app.py
2. **ทดสอบในโหมด Mock** ก่อน
3. **Implement MT5 Integration** จริง
4. **ทดสอบกับ MT5 Bridge** บน Windows VPS

ต้องการให้ผมช่วย implement ส่วนไหนเพิ่มเติมไหมครับ?
