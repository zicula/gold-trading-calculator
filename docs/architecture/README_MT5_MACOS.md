# การเชื่อมต่อ MT5 บน macOS

## 🍎 ความท้าทายสำหรับ macOS

MetaTrader 5 Python API (MetaTrader5) ทำงานได้เฉพาะบน Windows เท่านั้น สำหรับ macOS จะต้องใช้วิธีพิเศษ

## 💡 วิธีแก้ปัญหา

### **วิธีที่ 1: Windows Virtual Machine (แนะนำ)**

#### 1.1 ติดตั้ง Parallels Desktop
```bash
# ดาวน์โหลดและติดตั้ง Parallels Desktop
# https://www.parallels.com/products/desktop/
```

#### 1.2 ตั้งค่า Windows VM
- ติดตั้ง Windows 11 ใน Parallels
- ติดตั้ง MT5 ใน Windows VM
- ติดตั้ง Python และ MetaTrader5 library

#### 1.3 เรียกใช้ Server ใน Windows VM
```cmd
# ใน Windows VM
cd /path/to/project
pip install MetaTrader5 Flask flask-cors
python mt5_server.py
```

#### 1.4 เชื่อมต่อจาก macOS
```javascript
// จาก macOS Safari/Chrome เข้าถึง VM IP
const MT5_SERVER = 'http://192.168.1.100:8080';  // IP ของ Windows VM
```

---

### **วิธีที่ 2: Wine + MT5 (ซับซ้อน)**

#### 2.1 ติดตั้ง Wine
```bash
# ติดตั้ง Wine ผ่าน Homebrew
brew install --cask wine-stable
```

#### 2.2 ติดตั้ง MT5 ผ่าน Wine
```bash
# ดาวน์โหลด MT5 Windows version
# รันผ่าน Wine (อาจมีปัญหา)
wine mt5setup.exe
```

---

### **วิธีที่ 3: Docker Desktop + Windows Container**

#### 3.1 ติดตั้ง Docker Desktop
```bash
# ดาวน์โหลดและติดตั้ง Docker Desktop สำหรับ Mac
# https://www.docker.com/products/docker-desktop/
```

#### 3.2 สร้าง Windows Container
```dockerfile
# Dockerfile.windows
FROM mcr.microsoft.com/windows:1809

# Install Python and MT5
RUN powershell -Command \
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe" -OutFile "python-installer.exe" ; \
    Start-Process python-installer.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait

# Copy and run MT5 server
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "mt5_server.py"]
```

---

### **วิธีที่ 4: Remote MT5 Server (ง่ายที่สุด)**

#### 4.1 ใช้ VPS Windows
- เช่า VPS Windows (AWS EC2, Google Cloud, Azure)
- ติดตั้ง MT5 และ Python บน VPS
- รัน MT5 Server บน VPS
- เชื่อมต่อจาก macOS ผ่าน Internet

#### 4.2 แก้ไข Configuration
```javascript
// ใน mt5_integration.html
const MT5_SERVER_URL = 'https://your-vps-ip:8080';
```

---

## 🚀 **แนะนำ: ใช้ Parallels Desktop**

### **ข้อดี:**
- ✅ ง่ายที่สุด
- ✅ เสถียรที่สุด
- ✅ MT5 ทำงานได้เต็มประสิทธิภาพ
- ✅ สามารถ share network ได้

### **ข้อเสีย:**
- ❌ ต้องซื้อ Parallels Desktop (~$99)
- ❌ ใช้ RAM และ Storage มาก

---

## 📋 **ขั้นตอนการติดตั้ง Parallels**

### 1. ติดตั้ง Parallels Desktop
```bash
# ดาวน์โหลดจาก https://www.parallels.com/
# ติดตั้งตามขั้นตอน
```

### 2. สร้าง Windows VM
- เปิด Parallels Desktop
- คลิก "Create New Virtual Machine"
- เลือก "Install Windows"
- ติดตั้ง Windows 11

### 3. ติดตั้ง MT5 ใน Windows VM
```cmd
# ดาวน์โหลด MT5 จาก https://www.metatrader5.com/
# ติดตั้งและเข้าสู่ระบบ account ของคุณ
```

### 4. ติดตั้ง Python Environment
```cmd
# ติดตั้ง Python 3.11
# ติดตั้ง dependencies
pip install MetaTrader5 Flask flask-cors requests
```

### 5. Copy โปรเจกต์ไป Windows VM
```cmd
# Copy โฟลเดอร์ Gold_Trading_Calculator ไป Windows VM
# หรือ clone จาก GitHub
git clone https://github.com/zicula/gold-trading-calculator.git
```

### 6. รัน MT5 Server
```cmd
cd gold-trading-calculator
python mt5_server.py
```

### 7. หา IP ของ Windows VM
```cmd
# ใน Windows VM
ipconfig
# จดบันทึก IP Address (เช่น 10.211.55.4)
```

### 8. แก้ไข Configuration บน macOS
```javascript
// ใน mt5_integration.html (บน macOS)
const MT5_SERVER_URL = 'http://10.211.55.4:8080';  // IP ของ Windows VM
```

---

## 🧪 **ทดสอบการเชื่อมต่อ**

### 1. เปิด MT5 ใน Windows VM
### 2. รัน mt5_server.py ใน Windows VM
### 3. เปิด mt5_integration.html บน macOS
### 4. ทดสอบการเชื่อมต่อ

---

## 🔧 **Troubleshooting**

### ปัญหา: ไม่สามารถเชื่อมต่อได้
```bash
# ตรวจสอบ Firewall ใน Windows VM
# เปิด Port 8080 ใน Windows Firewall
```

### ปัญหา: MT5 ไม่เชื่อมต่อ
```python
# ตรวจสอบ Auto Trading ใน MT5
# Tools > Options > Expert Advisors > Allow automated trading
```

### ปัญหา: Network ไม่เข้าถึงได้
```bash
# ใน Parallels Desktop
# VM Configuration > Hardware > Network > Shared Network
```

---

## 💰 **ทางเลือกฟรี**

หากไม่ต้องการซื้อ Parallels สามารถใช้:
- **UTM** (ฟรี): https://mac.getutm.app/
- **VirtualBox** (ฟรี): https://www.virtualbox.org/
- **VMware Fusion** (มีใบอนุญาตฟรีสำหรับบางกรณี)

---

## 📞 **ความช่วยเหลือ**

หากต้องการความช่วยเหลือเพิ่มเติม สามารถ:
1. ดู Log ใน mt5_server.log
2. ตรวจสอบ MT5 Expert Advisors settings
3. ทดสอบ API ผ่าน /status endpoint
