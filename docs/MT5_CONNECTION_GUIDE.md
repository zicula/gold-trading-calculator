# การเชื่อมต่อ MT5 กับ Gold Trading Calculator บน VPS

## 🔍 ภาพรวมปัญหา

MetaTrader 5 (MT5) **ทำงานได้เฉพาะ Windows** ในขณะที่ DigitalOcean VPS ใช้ Ubuntu Linux ดังนั้นเราต้องมีวิธีแก้ปัญหาพิเศษ

## 🛠️ วิธีแก้ปัญหา: 3 ตัวเลือก

### ✅ Option 1: Mock Mode (สำหรับ Testing)
```bash
# ระบบจะทำงานโดยจำลองข้อมูล MT5
# เหมาะสำหรับ demo และ testing
curl http://YOUR_VPS_IP:8080/api/status
# Response: "mt5_mode": "mock"
```

### 🖥️ Option 2: Windows VPS (สำหรับ Production)
ใช้ Windows Server VPS แยกต่างหาก:
- สร้าง Windows Droplet บน DigitalOcean
- ติดตั้ง MT5 และ Python
- รัน MT5 Bridge Server

### 🔗 Option 3: Hybrid Setup (แนะนำ)
- **Ubuntu VPS**: รัน Web Application
- **Windows VPS/PC**: รัน MT5 Bridge

## 🚀 Setup Hybrid แบบ Step-by-Step

### Step 1: Ubuntu VPS (Web App)
```bash
# ใช้ VPS_SETUP_GUIDE.md ที่มีอยู่แล้ว
docker-compose -f deploy/docker/docker-compose.yml up -d
```

### Step 2: Windows VPS/PC (MT5 Bridge)

#### A. สร้าง Windows Droplet (DigitalOcean)
1. เลือก **Windows Server 2019/2022**
2. ขนาด: **4GB RAM** ขึ้นไป
3. Remote Desktop เข้าไป

#### B. ติดตั้ง Software บน Windows
```powershell
# 1. ติดตั้ง Python
# Download จาก python.org

# 2. ติดตั้ง MetaTrader 5
# Download จาก broker ของคุณ

# 3. ติดตั้ง Python packages
pip install MetaTrader5 flask flask-cors python-dotenv
```

#### C. ดาวน์โหลดโปรเจ็ค
```powershell
git clone https://github.com/zicula/gold-trading-calculator.git
cd gold-trading-calculator
```

#### D. ตั้งค่า API Key
```powershell
# สร้างไฟล์ .env
echo MT5_BRIDGE_API_KEY=your-super-secret-key > .env
```

#### E. รัน MT5 Bridge Server
```powershell
python scripts/mt5_bridge_server.py
```

### Step 3: เชื่อมต่อ Ubuntu VPS กับ Windows Bridge

#### A. แก้ไข Environment บน Ubuntu VPS
```bash
# SSH เข้า Ubuntu VPS
ssh root@YOUR_UBUNTU_VPS_IP

# แก้ไขไฟล์ .env
nano .env

# เพิ่ม:
MT5_BRIDGE_URL=http://WINDOWS_VPS_IP:8081
MT5_BRIDGE_API_KEY=your-super-secret-key
MT5_MODE=bridge
```

#### B. Restart Web Application
```bash
docker-compose -f deploy/docker/docker-compose.yml down
docker-compose -f deploy/docker/docker-compose.yml up -d
```

## 🔐 การเชื่อมต่อ MT5 Accounts

### ผ่าน Web Interface:
1. เข้า `http://YOUR_UBUNTU_VPS_IP:8080`
2. Login เข้าระบบ
3. ไปที่ **Account Management**
4. คลิก **Add MT5 Account**
5. กรอกข้อมูล:
   - **Account Name**: ชื่อที่ต้องการ
   - **Login**: หมายเลขบัญชี MT5
   - **Password**: รหัสผ่าน MT5
   - **Server**: เซิร์ฟเวอร์ broker

### ผ่าน API:
```bash
curl -X POST http://YOUR_UBUNTU_VPS_IP:8080/api/accounts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "account_name": "Live Account 1",
    "login": "12345678",
    "password": "your-mt5-password",
    "server": "YourBroker-Live",
    "account_type": "live"
  }'
```

## ⚡ การทดสอบการเชื่อมต่อ

### 1. ทดสอบ MT5 Bridge
```bash
# ตรวจสอบสถานะ MT5 Bridge
curl -H "X-API-Key: your-super-secret-key" \
     http://WINDOWS_VPS_IP:8081/health

# Response ควรได้:
{
  "status": "running",
  "mt5_available": true,
  "connected_accounts": 0
}
```

### 2. ทดสอบการเชื่อมต่อ Account
```bash
# Connect MT5 Account
curl -X POST http://WINDOWS_VPS_IP:8081/mt5/connect \
  -H "X-API-Key: your-super-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "12345678",
    "password": "your-password",
    "server": "YourBroker-Live",
    "account_name": "Live Account 1"
  }'
```

### 3. ทดสอบ Web Application
```bash
# ตรวจสอบสถานะระบบ
curl http://YOUR_UBUNTU_VPS_IP:8080/api/status

# Response ควรมี:
{
  "status": "running",
  "mt5_mode": "bridge",
  "mt5_bridge_status": "connected"
}
```

## 🔧 การแก้ปัญหาทั่วไป

### ❌ MT5 Bridge ไม่ทำงาน
```powershell
# 1. ตรวจสอบ MT5 ว่าเปิดอยู่
# 2. ตรวจสอบ Auto Trading เปิดอยู่
# 3. ตรวจสอบ Windows Firewall
netsh advfirewall firewall add rule name="MT5 Bridge" dir=in action=allow protocol=TCP localport=8081
```

### ❌ Ubuntu VPS เชื่อมต่อ Bridge ไม่ได้
```bash
# 1. ตรวจสอบ Network ระหว่าง VPS
ping WINDOWS_VPS_IP

# 2. ตรวจสอบ port 8081 เปิดอยู่
telnet WINDOWS_VPS_IP 8081

# 3. ดู logs
docker-compose logs -f web
```

### ❌ MT5 Login ไม่ได้
1. ตรวจสอบ Login/Password/Server ถูกต้อง
2. ตรวจสอบ MT5 สามารถ login manual ได้
3. ตรวจสอบ Auto Trading เปิดอยู่

## 💰 ตัวอย่างการใช้งานจริง

### สร้างบัญชี MT5 ใหม่:
```javascript
// ผ่าน Web Interface
fetch('/api/accounts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    account_name: 'Live Gold Trading',
    login: '12345678',
    password: 'mt5-password',
    server: 'YourBroker-Live',
    account_type: 'live'
  })
})
```

### คำนวณ Lot Size:
```javascript
// ข้อมูลจะถูกดึงจาก MT5 จริง
const calculation = await fetch('/api/calculate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    account_id: 1,
    risk_percentage: 2,
    stop_loss_pips: 50,
    symbol: 'XAUUSD'
  })
})
```

## 📊 Architecture ของระบบ

```
Internet
    ↓
Ubuntu VPS (DigitalOcean)
├── Nginx (Port 80/443)
├── Web Application (Port 8080)
├── Redis (Port 6379)
└── SQLite Database
    ↓ HTTP API
Windows VPS/PC
├── MT5 Bridge Server (Port 8081)
├── MetaTrader 5
└── MT5 Bridge API
    ↓ TCP Connection
Broker Servers
```

## 🔒 Security Best Practices

1. **VPN**: ตั้ง VPN ระหว่าง Ubuntu กับ Windows VPS
2. **SSL**: ใช้ HTTPS certificates
3. **Firewall**: เปิดเฉพาะ port ที่จำเป็น
4. **API Keys**: ใช้ strong API keys
5. **Regular Updates**: อัปเดต OS และ software เป็นประจำ

## 💡 Tips สำหรับ Production

- **Monitoring**: ตั้ง monitoring สำหรับทั้ง VPS
- **Backups**: สำรองข้อมูล database อัตโนมัติ
- **Load Balancing**: ใช้หลาย Windows VPS สำหรับ MT5
- **Redundancy**: มี backup MT5 Bridge server

---

**🎯 สรุป**: ด้วยวิธี Hybrid Setup คุณจะได้ระบบที่:
- ✅ ทำงานได้เต็มรูปแบบกับ MT5 จริง
- ✅ ใช้ Linux VPS ประหยัดต้นทุน
- ✅ มีความยืดหยุ่นสูง
- ✅ ปลอดภัยและเสถียร
