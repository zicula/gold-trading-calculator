# GitHub Pages Setup Guide

## 🔧 วิธีเปิด GitHub Pages

### Step 1: เข้าไปที่ GitHub Repository
1. ไปที่ https://github.com/zicula/gold-trading-calculator
2. คลิก **Settings** tab (ทางขวาบน)

### Step 2: เปิด GitHub Pages
1. Scroll ลงไปหา **Pages** ในเมนูซ้าย
2. คลิก **Pages**

### Step 3: Configure Source
1. ในส่วน **Source**:
   - เลือก **Deploy from a branch**
2. ในส่วน **Branch**:
   - เลือก **main** (หรือ **master**)
   - เลือก **/ (root)**
3. คลิก **Save**

### Step 4: รอการ Deploy
- GitHub จะใช้เวลา 2-10 นาที ในการ build
- URL จะเป็น: `https://zicula.github.io/gold-trading-calculator/`

## 🔄 Alternative: Manual Enable Steps

### ถ้าไม่เจอ Pages ใน Settings:
1. เข้า Repository Settings
2. Scroll ลงไปข้างล่างสุด
3. หา **Danger Zone** → **Change repository visibility**
4. ตรวจสอบว่า repository เป็น **Public**
5. GitHub Pages ใช้ได้เฉพาะ Public repos (ใน free plan)

## 📋 Checklist:
- [ ] Repository เป็น Public
- [ ] มีไฟล์ index.html ใน root
- [ ] เปิด GitHub Pages ใน Settings → Pages
- [ ] เลือก Source: Deploy from branch
- [ ] เลือก Branch: main
- [ ] รอ 2-10 นาที สำหรับ deployment

## 🎯 Expected URLs หลัง Enable:
- Main: https://zicula.github.io/gold-trading-calculator/
- Risk Calculator: https://zicula.github.io/gold-trading-calculator/frontend/components/risk_calculator.html

## 🚨 Troubleshooting:
- Repository ต้องเป็น Public
- Branch ต้องมีไฟล์ index.html
- รอ deployment เสร็จก่อน (ดูใน Actions tab)
