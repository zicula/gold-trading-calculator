# Documentation - Gold Trading Calculator

## 📚 เอกสารประกอบโปรเจ็ค

### 📁 โครงสร้าง

```
docs/
├── guides/                # คู่มือการใช้งาน
│   ├── getting-started.md        # เริ่มต้นใช้งาน
│   ├── broadcast-guide.md        # คู่มือ Broadcast
│   ├── digitalocean-setup-guide.md # ตั้งค่า DigitalOcean
│   ├── vps-setup-guide.md        # ตั้งค่า VPS
│   ├── deployment-guide.md       # คู่มือ Deploy
│   ├── github-pages-setup.md     # ตั้งค่า GitHub Pages
│   ├── github-secrets-setup.md   # ตั้งค่า GitHub Secrets
│   ├── quick-deploy.md           # Deploy อย่างรวดเร็ว
│   ├── quick-start-digitalocean.md # เริ่มใช้ DigitalOcean
│   ├── deploy.md                 # คู่มือ Deploy ทั่วไป
│   ├── github-vps-options.md     # ตัวเลือก VPS
│   └── vps-compatibility-analysis.md # วิเคราะห์ VPS
├── api/                   # เอกสาร API
│   ├── authentication.md  # API Authentication
│   ├── accounts.md        # Accounts API
│   ├── calculator.md      # Calculator API
│   └── broadcast.md       # Broadcast API
├── architecture/          # เอกสารสถาปัตยกรรม
│   ├── hybrid-architecture.md    # สถาปัตยกรรม Hybrid
│   ├── database-schema.md        # โครงสร้างฐานข้อมูล
│   ├── security-model.md         # โมเดลความปลอดภัย
│   ├── deployment-architecture.md # สถาปัตยกรรม Deploy
│   └── readme-mt5-macos.md       # MT5 บน macOS
├── business/              # เอกสารธุรกิจ
│   ├── business-requirements-mt5.md # ความต้องการทางธุรกิจ
│   ├── requirements.md           # ความต้องการระบบ
│   └── user-stories.md           # User Stories
├── INSTRUCTION_PROMPTS.md # คำสั่งสำหรับ AI
├── PROMPT_HISTORY.md      # ประวัติการใช้ Prompt
├── CHANGELOG.md           # บันทึกการเปลี่ยนแปลง
└── README.md             # ไฟล์นี้
```

## 🎯 ประเภทเอกสาร

### 👥 สำหรับผู้ใช้งาน
- **getting-started.md** - เริ่มต้นใช้งานระบบ
- **broadcast-guide.md** - คู่มือใช้งาน Broadcast Mode
- **API Documentation** - เอกสาร API สำหรับนักพัฒนา

### 🔧 สำหรับผู้ดูแลระบบ
- **VPS Setup Guides** - คู่มือตั้งค่า VPS และ Deploy
- **GitHub Setup Guides** - คู่มือตั้งค่า GitHub และ CI/CD
- **Security Documentation** - คู่มือความปลอดภัย

### 🏗️ สำหรับนักพัฒนา
- **Architecture Documentation** - สถาปัตยกรรมระบบ
- **Database Schema** - โครงสร้างฐานข้อมูล
- **Business Requirements** - ความต้องการทางธุรกิจ

## 📖 คู่มือหลัก

### 🚀 เริ่มต้นใช้งาน
1. อ่าน [getting-started.md](guides/getting-started.md)
2. ตั้งค่า VPS ตาม [vps-setup-guide.md](guides/vps-setup-guide.md)
3. Deploy ตาม [deployment-guide.md](guides/deployment-guide.md)

### 📡 Broadcast Mode
1. อ่าน [broadcast-guide.md](guides/broadcast-guide.md)
2. ตั้งค่า Roles และ Permissions
3. ทดสอบกับบัญชี Demo

### 🔧 Development
1. อ่าน [hybrid-architecture.md](architecture/hybrid-architecture.md)
2. ศึกษา [database-schema.md](architecture/database-schema.md)
3. ดู [business-requirements-mt5.md](business/business-requirements-mt5.md)

## 🔍 การค้นหาเอกสาร

### ตามหัวข้อ
- **Setup & Deployment**: `guides/`
- **API Reference**: `api/`
- **Technical Details**: `architecture/`
- **Business Logic**: `business/`

### ตามผู้ใช้
- **End Users**: `guides/getting-started.md`, `guides/broadcast-guide.md`
- **System Admins**: `guides/*setup*.md`, `guides/*deploy*.md`
- **Developers**: `architecture/`, `api/`, `business/`

## 📝 การอัปเดตเอกสาร

### เมื่อเพิ่มฟีเจอร์ใหม่
1. อัปเดต User Guide ใน `guides/`
2. เพิ่ม API Documentation ใน `api/`
3. อัปเดต Architecture ใน `architecture/`
4. บันทึกใน `CHANGELOG.md`

### เมื่อแก้ไข Bug
1. อัปเดต Troubleshooting Guide
2. แก้ไข Documentation ที่เกี่ยวข้อง
3. บันทึกใน `CHANGELOG.md`

### เมื่อเปลี่ยน Architecture
1. อัปเดต `architecture/`
2. แก้ไข Setup Guides
3. อัปเดต API Documentation
4. ทดสอบ Documentation

## 🎨 รูปแบบการเขียน

### Markdown Style
- ใช้ emoji สำหรับ headers (🎯, 🔧, 📝)
- ใช้ code blocks สำหรับ commands
- ใช้ tables สำหรับข้อมูลที่มีโครงสร้าง
- ใช้ links สำหรับอ้างอิง

### โครงสร้างเอกสาร
```markdown
# Title

## Overview
Brief description

## Prerequisites
What you need before starting

## Steps
1. Step one
2. Step two
3. Step three

## Troubleshooting
Common issues and solutions

## References
Links to related documentation
```

## 🔗 ลิงก์ที่เกี่ยวข้อง

- [Project Repository](https://github.com/zicula/gold-trading-calculator)
- [GitHub Pages](https://zicula.github.io/gold-trading-calculator)
- [DigitalOcean](https://www.digitalocean.com)
- [MetaTrader 5](https://www.metatrader5.com)
