# เริ่มต้นใช้งาน Hybrid Solution - Multi-Account MT5 Trading System

## 📋 ขั้นตอนการติดตั้งและใช้งาน

### 1. เตรียม VPS (DigitalOcean)
```bash
# ใช้ไฟล์ที่เตรียมไว้แล้ว
./setup_digitalocean_vps.ps1
```

### 2. ติดตั้ง Backend Server

#### 2.1 สร้างไดเรกทอรี backend
```bash
mkdir backend
cd backend
```

#### 2.2 ติดตั้ง Python packages
```bash
pip install -r requirements.txt
```

#### 2.3 ตั้งค่า Environment Variables
สร้างไฟล์ `.env`:
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_PATH=trading_accounts.db
ENCRYPTION_KEY=your-encryption-key-here
CORS_ORIGINS=https://zicula.github.io,https://your-domain.com
API_RATE_LIMIT=100
SESSION_TIMEOUT=24
PORT=8080
FLASK_ENV=production
```

#### 2.4 เริ่มใช้งาน Server
```bash
python multi_account_server.py
```

### 3. ตั้งค่า GitHub Pages

#### 3.1 อัปโหลด Frontend
- อัปโหลดไฟล์ `multi_account_calculator.html` ไป GitHub repository
- ตั้งค่า GitHub Pages ใน Settings
- ใช้งานได้ที่ `https://username.github.io/repository-name/`

#### 3.2 แก้ไข API URL
แก้ไขใน `multi_account_calculator.html`:
```javascript
const API_BASE = 'https://your-vps-ip:8080/api';
```

### 4. การใช้งาน

#### 4.1 สมัครสมาชิก
1. เปิดเว็บไซต์ที่ GitHub Pages
2. คลิก "สมัครสมาชิกใหม่"
3. กรอกข้อมูล: ชื่อผู้ใช้, อีเมล, รหัสผ่าน
4. เลือก Role:
   - **ผู้ใช้ทั่วไป**: ใช้งานปกติ เฉพาะตัวเอง
   - **ผู้ใช้ Broadcast**: รับคำสั่งจาก Super Admin
   - **Super Admin**: สามารถส่ง Broadcast ได้
5. คลิก "สมัครสมาชิก"

#### 4.2 เข้าสู่ระบบ
1. กรอกชื่อผู้ใช้และรหัสผ่าน
2. คลิก "เข้าสู่ระบบ"

#### 4.3 เพิ่มบัญชี MT5
1. คลิก "+ เพิ่มบัญชี MT5"
2. กรอกข้อมูล:
   - ชื่อบัญชี (ตั้งชื่อเอง)
   - Login MT5
   - รหัสผ่าน MT5
   - Server MT5
   - โบรกเกอร์ (ไม่จำเป็น)
   - ประเภทบัญชี (Demo/Real)
3. คลิก "เพิ่มบัญชี"

#### 4.4 เชื่อมต่อบัญชี
1. เลือกบัญชีที่ต้องการใช้งาน
2. คลิก "เชื่อมต่อ"
3. รอการเชื่อมต่อสำเร็จ (จุดสีเขียว)

#### 4.5 คำนวณและส่งคำสั่ง
1. กรอกข้อมูล Portfolio และ Risk
2. กรอก Entry Price และ Stop Loss
3. ตั้งค่า Take Profit
4. คลิก "คำนวณ"
5. คลิก "ส่งคำสั่งไป MT5"

#### 4.6 การใช้งาน Broadcast Mode (Super Admin เท่านั้น)
1. เข้าสู่ระบบด้วย account Super Admin
2. เลื่อนลงมาหาส่วน "ระบบ Broadcast Orders"
3. เปิดใช้งาน "Broadcast Mode"
4. ตั้งค่าการคำนวณตามปกติ
5. คลิก "Broadcast ไปทุก User" แทนการส่งปกติ
6. ยืนยันการส่ง Broadcast
7. ระบบจะส่งคำสั่งไปยังผู้ใช้ทุกคนที่มี role "broadcast"
8. คลิก "ตรวจสอบสถานะ Broadcast" เพื่อดูผลลัพธ์

## 🔐 ความปลอดภัย

### การเข้ารหัสข้อมูล
- รหัสผ่าน MT5 ถูกเข้ารหัสก่อนเก็บในฐานข้อมูล
- ใช้ JWT สำหรับการ Authentication
- Session timeout อัตโนมัติ

### การตรวจสอบสิทธิ์
- ทุก API call ต้องมี JWT token
- แยกบัญชีผู้ใช้อย่างชัดเจน
- Log การใช้งานทั้งหมด
- **Role-Based Access Control (RBAC)**

### การแยกบัญชี
- แต่ละผู้ใช้เห็นเฉพาะบัญชีของตัวเอง
- ไม่สามารถเข้าถึงข้อมูลผู้อื่นได้
- การเชื่อมต่อ MT5 แยกต่างหากทุกบัญชี

### ระบบ Broadcast Security
- เฉพาะ Super Admin เท่านั้นที่ส่ง Broadcast ได้
- ระบบยืนยันการส่ง Broadcast
- Audit log ทุกการใช้งาน Broadcast
- การแยก Role แบบเข้มงวด

## 🚀 การ Deploy

### ใช้ GitHub Actions (แนะนำ)
```yaml
# ไฟล์ .github/workflows/deploy.yml มีอยู่แล้ว
# แค่ push code ไป GitHub จะ deploy อัตโนมัติ
```

### Deploy Manual
```bash
# ใน VPS
git clone https://github.com/username/repository.git
cd repository/backend
pip install -r requirements.txt
python multi_account_server.py
```

## 📊 การตรวจสอบระบบ

### Health Check
```bash
curl http://your-vps-ip:8080/api/status
```

### ดู Log
```bash
tail -f backend/trading_server.log
```

### ตรวจสอบฐานข้อมูล
```bash
sqlite3 trading_accounts.db
.tables
SELECT * FROM users;
```

## 🔧 การแก้ไขปัญหา

### ปัญหาการเชื่อมต่อ MT5
1. ตรวจสอบ Login, Password, Server
2. ตรวจสอบว่า MT5 terminal เปิดอยู่ใน VPS
3. ตรวจสอบ Firewall settings

### ปัญหา CORS
1. ตรวจสอบ `CORS_ORIGINS` ใน environment
2. ใส่ URL ของ GitHub Pages
3. Restart server หลังแก้ไข

### ปัญหา Database
1. ตรวจสอบไฟล์ `trading_accounts.db`
2. ลบไฟล์แล้วให้ระบบสร้างใหม่
3. ตรวจสอบ permission ของไฟล์

## 📝 ข้อมูลเพิ่มเติม

### API Endpoints
- `POST /api/register` - สมัครสมาชิก (รองรับ role)
- `POST /api/login` - เข้าสู่ระบบ
- `GET /api/accounts` - ดูบัญชี MT5
- `POST /api/accounts` - เพิ่มบัญชี MT5
- `POST /api/accounts/:id/connect` - เชื่อมต่อบัญชี
- `POST /api/calculate` - คำนวณ lot size
- `POST /api/send_orders` - ส่งคำสั่งไป MT5
- `POST /api/broadcast_orders` - ส่ง Broadcast (Super Admin)
- `GET /api/broadcast_status` - ดูสถานะ Broadcast (Super Admin)
- `GET /api/status` - ตรวจสอบสถานะ

### Database Schema
```sql
-- Users table with role support
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    api_key VARCHAR(255) UNIQUE,
    role VARCHAR(20) DEFAULT 'user',  -- 'user', 'broadcast', 'super_admin'
    created_at TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Broadcast queue for managing mass orders
CREATE TABLE broadcast_queue (
    id INTEGER PRIMARY KEY,
    admin_user_id INTEGER,
    target_user_id INTEGER,
    order_data TEXT,
    status VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'executed', 'failed'
    created_at TIMESTAMP,
    executed_at TIMESTAMP,
    error_message TEXT
);

-- ดูรายละเอียดเพิ่มเติมใน HYBRID_ARCHITECTURE.md
```

### Security Features
- Password hashing (bcrypt)
- Data encryption (Fernet)
- JWT authentication
- Rate limiting
- Audit logging
- Session management
- **Role-based access control (RBAC)**
- **Broadcast security validation**
- **Multi-level authorization**

## 🎯 ขั้นตอนถัดไป

1. ทดสอบระบบด้วยบัญชี Demo
2. ตั้งค่า SSL Certificate สำหรับ HTTPS
3. ติดตั้ง Monitoring system
4. สำรองข้อมูลอัตโนมัติ
5. ปรับปรุง UI/UX ตามความต้องการ
6. **ทดสอบระบบ Broadcast กับผู้ใช้จริง**
7. **ตั้งค่า Role-based permissions เพิ่มเติม**

## 🚨 หมายเหตุสำคัญ - Broadcast Mode

⚠️ **คำเตือน**: ระบบ Broadcast Mode เป็นฟีเจอร์ที่มีพลังมาก โปรดใช้อย่างระมัดระวัง

### การใช้งาน Broadcast อย่างปลอดภัย:
1. **ตรวจสอบข้อมูล**: ตรวจสอบพารามิเตอร์ให้ถูกต้องก่อนส่ง Broadcast
2. **ทดสอบก่อน**: ทดสอบกับบัญชี Demo ก่อนใช้กับบัญชีจริง
3. **จำกัดผู้เข้าถึง**: ให้เฉพาะบุคคลที่เชื่อถือได้เท่านั้นเป็น Super Admin
4. **ตรวจสอบ Role**: ตรวจสอบให้แน่ใจว่าผู้ใช้ที่มี role "broadcast" ต้องการรับคำสั่งจริงๆ
5. **Monitoring**: ติดตามผลการดำเนินการ Broadcast อย่างสม่ำเสมอ

### User Roles ที่มี:
- **user**: ผู้ใช้ทั่วไป สามารถใช้งานเฉพาะตัวเองเท่านั้น
- **broadcast**: ผู้ใช้ที่ยินยอมรับคำสั่ง Broadcast จาก Super Admin
- **super_admin**: ผู้ดูแลระบบ สามารถส่ง Broadcast ให้ทุกคนได้

---

**หมายเหตุ:** ระบบนี้รองรับหลายบัญชี MT5 ต่อผู้ใช้หนึ่งคน และมีความปลอดภัยสูง เหมาะสำหรับการใช้งานจริงในการเทรด พร้อมฟีเจอร์ Broadcast ที่ทรงพลังสำหรับการจัดการกลุ่ม
