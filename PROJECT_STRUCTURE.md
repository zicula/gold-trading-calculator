# 📁 Project Structure - Gold Trading Calculator

This document provides a comprehensive overview of the project structure, explaining the purpose and organization of each component in the Gold Trading Calculator system.

## � Overview

```
Gold_Trading_Calculator/
├── 📁 backend/                 # Flask API server
├── 📁 frontend/               # Web interface files  
├── 📁 deploy/                 # Deployment configurations
├── 📁 tests/                  # Testing framework
├── 📁 docs/                   # Documentation
├── 📁 config/                 # Configuration files
├── 📁 scripts/                # Utility scripts
├── 📁 logs/                   # Application logs
├── 📄 *.html                  # Main application files
├── 📄 *.js                    # JavaScript utilities
└── 📄 *.md                    # Documentation files
```

## 🎯 ประโยชน์ของโครงสร้างใหม่

### 1. **แยกความรับผิดชอบชัดเจน**
- **Frontend**: UI/UX และ Client-side logic
- **Backend**: API, Business logic, Database
- **Deploy**: Infrastructure และ Deployment
- **Docs**: Documentation ทุกประเภท
- **Tests**: Test suites แยกตามประเภท

### 2. **ง่ายต่อการ Maintain**
- หาไฟล์ได้ง่าย ตามหน้าที่การทำงาน
- แก้ไขโค้ดไม่กระทบส่วนอื่น
- เพิ่มฟีเจอร์ใหม่ง่ายขึ้น

### 3. **รองรับการทำงานเป็นทีม**
- Developer สามารถแบ่งงานตาม folder
- Frontend/Backend แยกกันอย่างชัดเจน
- Documentation แยกตามผู้ใช้

### 4. **รองรับ Scaling**
- สามารถแยก Deploy แต่ละส่วนได้
- เพิ่ม Microservices ได้ง่าย
- Test และ Monitor แยกได้

## 🚀 การ Migration

### ขั้นตอนการย้ายไฟล์:
1. สร้าง folder structure ใหม่
2. ย้ายไฟล์ไปตำแหน่งใหม่
3. อัปเดต import paths
4. อัปเดต deployment scripts
5. อัปเดต documentation

### ไฟล์ที่ต้องอัปเดต:
- GitHub Actions workflows
- Import paths ใน Python
- Asset paths ใน HTML/CSS
- Documentation links
