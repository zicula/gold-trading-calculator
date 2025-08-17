# Broadcast Mode - User Guide

## 📡 ระบบ Broadcast Orders - คู่มือการใช้งาน

### 🎯 วัตถุประสงค์
ระบบ Broadcast Mode ช่วยให้ Super Admin สามารถส่งคำสั่งซื้อขาย (Trading Orders) ไปยังผู้ใช้หลายคนพร้อมกันได้ โดยผู้ใช้ที่มี role "broadcast" จะได้รับและดำเนินการตามคำสั่งโดยอัตโนมัติ

### 👥 User Roles ในระบบ

#### 1. **user** (ผู้ใช้ทั่วไป)
- ใช้งานระบบได้เฉพาะตัวเองเท่านั้น
- ไม่ได้รับคำสั่ง Broadcast
- ส่งคำสั่งไปยัง MT5 ของตัวเองเท่านั้น

#### 2. **broadcast** (ผู้ใช้ Broadcast)
- รับคำสั่ง Broadcast จาก Super Admin
- ระบบจะทำ order อัตโนมัติเมื่อได้รับ Broadcast
- ยังคงสามารถใช้งานปกติได้เหมือนผู้ใช้ทั่วไป
- ต้องมีบัญชี MT5 ที่เชื่อมต่ออยู่

#### 3. **super_admin** (ผู้ดูแลระบบ)
- สามารถส่ง Broadcast Orders ได้
- ดูสถิติและสถานะ Broadcast
- จัดการผู้ใช้ Broadcast
- ใช้งานระบบได้เหมือนผู้ใช้ทั่วไป

## 🚀 วิธีการใช้งาน Broadcast Mode

### สำหรับ Super Admin

#### 1. เข้าสู่ระบบ
```
- เข้าสู่ระบบด้วย account ที่มี role "super_admin"
- ระบบจะแสดง badge "👑 Super Admin"
- ส่วน "📡 ระบบ Broadcast Orders" จะปรากฏขึ้น
```

#### 2. เปิดใช้งาน Broadcast Mode
```
- เลื่อนลงไปหาส่วน "ระบบ Broadcast Orders"
- เปิดใช้งาน checkbox "🚀 เปิดใช้งาน Broadcast Mode"
- ข้อมูลเพิ่มเติมจะแสดงขึ้น
- ปุ่ม "📡 Broadcast ไปทุก User" จะปรากฏ
```

#### 3. ตั้งค่าพารามิเตอร์การเทรด
```
- กรอกข้อมูลเหมือนการใช้งานปกติ:
  * Symbol (XAUUSD, XAGUSD)
  * Entry Price
  * Stop Loss
  * Risk Percentage
  * Take Profit levels
```

#### 4. ส่ง Broadcast
```
- คลิกปุ่ม "📡 Broadcast ไปทุก User"
- ระบบจะแสดงข้อความยืนยัน
- อ่านคำเตือนให้ครบถ้วน
- คลิก "ตกลง" เพื่อดำเนินการ
```

#### 5. ตรวจสอบผลลัพธ์
```
- ระบบจะแสดงจำนวนผู้ใช้ที่ได้รับ Broadcast
- แสดงจำนวนการดำเนินการสำเร็จ
- คลิก "🔍 ตรวจสอบสถานะ Broadcast" เพื่อดูรายละเอียด
```

### สำหรับ Broadcast Users

#### การตั้งค่าบัญชี
```
1. สมัครสมาชิกด้วย role "broadcast"
2. เพิ่มบัญชี MT5 ในระบบ
3. เชื่อมต่อบัญชี MT5 ให้พร้อมใช้งาน
4. ระบบจะแสดง badge "📡 Broadcast User"
```

#### เมื่อได้รับ Broadcast
```
- ระบบจะดำเนินการอัตโนมัติ
- คำนวณ lot size ตามพอร์ตของผู้ใช้
- ส่งคำสั่งไปยัง MT5 ที่เชื่อมต่ออยู่
- บันทึก log การดำเนินการ
```

## 🔧 การตั้งค่าเทคนิค

### Database Migration (เพิ่ม role column)
```sql
-- เพิ่ม column role ในตาราง users
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user';

-- สร้างตาราง broadcast_queue
CREATE TABLE broadcast_queue (
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
);
```

### Environment Variables
```env
# เพิ่มในไฟล์ .env
BROADCAST_ENABLED=true
BROADCAST_MAX_USERS=100
BROADCAST_TIMEOUT_SECONDS=300
```

## 📊 API Documentation

### POST /api/broadcast_orders
```json
// Request (Super Admin only)
{
    "symbol": "XAUUSD",
    "entryPrice1": "2650.00",
    "stopLoss": "2640.00",
    "riskPercent": "2",
    "portfolioSize": "1000",
    "tp1": "2660.00",
    "tp2": "2670.00",
    "tp3": "2680.00"
}

// Response
{
    "message": "Broadcast orders sent successfully",
    "target_users": 5,
    "executed_successfully": 4,
    "timestamp": "2025-08-17T10:30:00Z"
}
```

### GET /api/broadcast_status
```json
// Response (Super Admin only)
{
    "broadcast_statistics": [
        {
            "status": "executed",
            "count": 15,
            "latest": "2025-08-17T10:30:00Z"
        },
        {
            "status": "failed",
            "count": 2,
            "latest": "2025-08-17T09:15:00Z"
        }
    ],
    "broadcast_users": [
        {
            "id": 5,
            "username": "trader001",
            "last_login": "2025-08-17T09:00:00Z",
            "is_active": true
        }
    ]
}
```

## ⚠️ ข้อควรระวัง

### ความปลอดภัย
1. **จำกัดสิทธิ์**: ให้เฉพาะคนที่เชื่อถือได้เป็น Super Admin
2. **ทดสอบก่อน**: ทดสอบกับบัญชี Demo ก่อนใช้จริง
3. **ตรวจสอบพารามิเตอร์**: ตรวจสอบความถูกต้องก่อนส่ง Broadcast
4. **Monitoring**: ติดตามผลการดำเนินการอย่างสม่ำเสมอ

### ความเสี่ยง
1. **Mass Orders**: การส่ง Broadcast จะส่งผลต่อผู้ใช้หลายคน
2. **Market Impact**: Order จำนวนมากอาจส่งผลต่อตลาด
3. **Network Issues**: ปัญหาเครือข่ายอาจทำให้บางคนไม่ได้รับ Broadcast
4. **MT5 Connection**: ผู้ใช้ต้องเชื่อมต่อ MT5 ให้พร้อมใช้งาน

### Best Practices
1. **ประกาศล่วงหน้า**: แจ้งผู้ใช้ Broadcast ก่อนส่งคำสั่ง
2. **เวลาที่เหมาะสม**: ส่ง Broadcast ในช่วงเวลาเทรดที่เหมาะสม
3. **ขนาด Portfolio**: พิจารณาขนาด Portfolio ของผู้ใช้แต่ละคน
4. **Stop Loss**: ตั้ง Stop Loss ที่เหมาะสมเสมอ

## 🔍 การตรวจสอบและ Debug

### Log Files
```bash
# ดู log การใช้งาน Broadcast
grep "broadcast" /opt/trading/logs/trading_server.log

# ดู audit log
sqlite3 trading_accounts.db "SELECT * FROM audit_log WHERE action LIKE '%broadcast%'"
```

### Status Monitoring
```bash
# ตรวจสอบ broadcast queue
sqlite3 trading_accounts.db "SELECT * FROM broadcast_queue WHERE created_at > datetime('now', '-1 hour')"

# ดูสถิติ user roles
sqlite3 trading_accounts.db "SELECT role, COUNT(*) FROM users GROUP BY role"
```

---

**หมายเหตุ**: ระบบ Broadcast Mode เป็นเครื่องมือที่ทรงพลัง โปรดใช้อย่างรอบคอบและรับผิดชอบ
