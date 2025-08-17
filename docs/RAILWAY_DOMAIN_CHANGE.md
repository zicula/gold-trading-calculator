# 🚀 การเปลี่ยน Railway Domain เป็น zic-trading.up.railway.app

## ขั้นตอนการเปลี่ยน Domain บน Railway (ฟรี)

### Step 1: เข้าไปที่ Railway Dashboard
1. ไปที่ [railway.app](https://railway.app)
2. **Login** ด้วย GitHub account
3. **เลือก Project** `gold-trading-calculator`

### Step 2: เปลี่ยน Domain
1. **ไปที่ Settings** (เฟืองทางขวาบน)
2. **คลิกแท็บ "Domains"**
3. **หา Current Domain**: `web-production-15d0.up.railway.app`
4. **คลิก "Generate Domain"** หรือ **"Custom Domain"**
5. **ใส่ชื่อใหม่**: `zic-trading`
6. **Domain จะเป็น**: `zic-trading.up.railway.app`
7. **คลิก "Add Domain"**

### Step 3: ทดสอบ Domain ใหม่
ใน 1-2 นาที คุณจะเข้าได้ที่:
```
https://zic-trading.up.railway.app
```

---

## 🔧 การอัปเดต Environment Variables

### ใน Railway Dashboard → Variables:
อัปเดตค่าเหล่านี้:
```env
CORS_ORIGINS=https://zic-trading.up.railway.app
```

### หรือเพิ่ม Multiple Domains (แนะนำ):
```env
CORS_ORIGINS=https://zic-trading.up.railway.app,https://web-production-15d0.up.railway.app
```

---

## 📋 Checklist หลังเปลี่ยน Domain:

### ✅ ทดสอบการทำงาน:
1. **เข้าไปที่**: `https://zic-trading.up.railway.app`
2. **ทดสอบ API**: `https://zic-trading.up.railway.app/api/status`
3. **ทดสอบ Login/Register**
4. **ทดสอบ Calculator functions**

### ✅ อัปเดต Links (ถ้ามี):
- Documentation links
- README.md
- Social media/bookmarks

---

## 🎯 ผลลัพธ์ที่ได้:

### ก่อน:
```
https://web-production-15d0.up.railway.app
```

### หลัง:
```
https://zic-trading.up.railway.app
```

### ข้อดี:
- ✅ **ชื่อดูดี**: เข้าใจง่าย, จำง่าย
- ✅ **Professional**: ดู brand มากขึ้น  
- ✅ **ฟรี**: ไม่เสียค่าใช้จ่าย
- ✅ **SSL**: HTTPS อัตโนมัติ

---

## 🚨 หมายเหตุสำคัญ:

### การเปลี่ยน Domain:
- **Old domain** อาจจะยังใช้ได้ชั่วคราว
- **New domain** จะใช้ได้ทันทีหลังจากเปลี่ยน
- **SSL Certificate** จะ generate อัตโนมัติ

### ถ้ามีปัญหา:
1. **รอ 5-10 นาที** สำหรับ DNS propagation
2. **Clear browser cache** (Ctrl+F5)
3. **ลองใน Incognito mode**
4. **ตรวจสอบ CORS_ORIGINS** ใน Environment Variables

---

## 🔄 การ Rollback (ถ้าจำเป็น):

ถ้าต้องการเปลี่ยนกลับ:
1. **Railway Dashboard** → **Settings** → **Domains**
2. **Remove current domain**
3. **Generate new domain** หรือใช้ old domain
4. **อัปเดต CORS_ORIGINS** ใหม่

---

**🎉 พร้อมเปลี่ยนเป็น `zic-trading.up.railway.app` แล้ว!**

ทำตามขั้นตอนด้านบน แล้วแจ้งผลลัพธ์มาครับ!
