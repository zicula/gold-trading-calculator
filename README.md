# 🟡 Gold Trading Calculator V5.1.0 - Binance Style (by Zic)

เครื่องคำนวณการเทรดทองแบบครอบคลุม พร้อมระบบคำนวณ All In และ Risk Calculator สไตล์ Binance

## 🎯 คุณสมบัติหลัก

### 🚀 ฟีเจอร์ใหม่ V5.1.0 (Risk Calculator Enhancement & UI Improvements)

#### 🎯 **Risk Calculator Enhancements**
- **💰 Profit Display in TP Levels** - แสดงกำไรแต่ละ TP level (เช่น TP1 +5.0 $)
- **🎨 Enhanced Visual Design** - Highlight กำไรด้วยสีเขียวและพื้นหลัง
- **🔧 Fixed Zone Calculation Logic** - แก้ไขการจัดลำดับ zone ให้ถูกต้อง:
  - **Buy**: Zone เริ่มจากราคาสูง → ราคาต่ำ (3004 → 3000)
  - **Sell**: Zone เริ่มจากราคาต่ำ → ราคาสูง (3000 → 3004)
- **📐 Improved Column Width** - รองรับตัวเลข 4 หลักพร้อม 1 ทศนิยม
- **🔄 Side-by-Side Zone Layout** - Zone แสดงแบบซ้าย-ขวาทุกขนาดหน้าจอ

#### 🎨 **UI/UX Improvements**
- **✨ Clean Profit Display** - เอาวงเล็บออกจากกำไร เพื่อความอ่านง่าย
- **🎯 Visual Highlighting** - เพิ่มพื้นหลังสีเขียวให้ตัวเลขกำไร
- **📱 Mobile-First Layout** - Zone แสดงแนวนอนแม้ในหน้าจอ iPhone
- **💻 Responsive Grid System** - ระบบ layout ยืดหยุ่นทุกขนาดหน้าจอ
- **🔧 Fixed CSS Syntax** - แก้ไข CSS error เพื่อประสิทธิภาพที่ดีขึ้น

### 🚀 ฟีเจอร์ใหม่ V5.0.0 (Risk Calculator & Navigation System)

#### 📊 **Risk Calculator** (หน้าใหม่)
- **🎯 Risk-Based Lot Calculation** - คำนวณขนาด Lot จากเปอร์เซ็นต์ความเสี่ยงของพอร์ต
- **💰 Portfolio Risk Management** - ระบุขนาดพอร์ต (USD) และ % ความเสี่ยงที่ยอมรับได้
- **🔄 Dual-Zone Order Distribution** - แบ่งออเดอร์เป็น 2 โซนตามราคาที่กำหนด
- **⚖️ Percentage Allocation** - กำหนดสัดส่วนการแบ่งออเดอร์ (ค่าเริ่มต้น 30%/70%)
- **📈 Multi-TP Support** - รองรับ Take Profit ถึง 6 เลเวล
- **📋 Zone-Specific Analysis** - แสดง R:R และ Points แยกตามแต่ละโซน
- **🧠 Smart Zone Logic** - จัดลำดับโซนอัตโนมัติตามทิศทางการเทรด

#### 🧭 **Navigation System**
- **🔗 Inter-Page Navigation** - เมนูสำหรับสลับระหว่าง All-In Calculator และ Risk Calculator
- **🌐 Unified Language Switcher** - ปุ่มเปลี่ยนภาษาย้ายมาอยู่ในเมนูด้านขวา
- **📱 Compact Menu Design** - ออกแบบให้ไม่ต้อง scroll แนวนอนในมือถือ
- **🎨 Consistent UI/UX** - ระบบดีไซน์เดียวกันทั้ง 2 หน้า

#### 🔧 **Technical Improvements**
- **⚡ Corrected Zone Logic** - แก้ไขการคำนวณโซนราคาให้ถูกต้องตามทิศทางการเทรด
  - **Buy**: เริ่มซื้อจากราคาสูง → ราคาต่ำ
  - **Sell**: เริ่มขายจากราคาต่ำ → ราคาสูง
- **📐 Enhanced Validation** - ปรับปรุงการตรวจสอบข้อมูลสำหรับ price range
- **💾 Data Persistence** - บันทึกการตั้งค่าผู้ใช้ใน localStorage

### 🚀 ฟีเจอร์ใหม่ V4.7.0 (Language Switcher)
- **🌐 Multi-Language Support** - รองรับภาษาไทยและอังกฤษ
- **🔄 Language Toggle** - ปุ่มเปลี่ยนภาษา TH/EN แบบเรียลไทม์
- **💾 Language Persistence** - จำค่าภาษาที่เลือกไว้ใน localStorage
- **📋 Complete Translation** - แปลทุกองค์ประกอบ UI อย่างครบถ้วน
- **⚡ Instant Switch** - เปลี่ยนภาษาทันทีไม่ต้องรีโหลดหน้า

### 🚀 ฟีเจอร์ใหม่ V4.6.1 (Statistics Tracking)
- **📊 Usage Statistics** - ติดตามสถิติการใช้งานแบบเรียลไทม์
- **👁️ Page Views** - นับยอดเข้าชมหน้าเว็บ
- **👥 Unique Users** - ระบบนับผู้ใช้งานเฉพาะรายวัน
- **💾 Local Storage** - บันทึกข้อมูลสถิติในเครื่อง
- **🎨 Non-intrusive Display** - แสดงผลที่ไม่รบกวนเนื้อหาหลัก

### 🚀 ฟีเจอร์ใหม่ V4.4 (Project Ownership & Enhanced Responsive)
- **Project Branding** - เพิ่ม "by Zic" เพื่อแสดงความเป็นเจ้าของโปรเจ็กต์
- **Enhanced Responsive Design** - ปรับปรุงการแสดงผลทุกขนาดหน้าจอ
- **Better User Experience** - ปรับปรุงประสบการณ์ผู้ใช้โดยรวม
- **Professional Branding** - เพิ่มการแสดงผล branding ที่เหมาะสม

### 🚀 ฟีเจอร์ใหม่ V4.3 (Enhanced Card Display)
- **Pips Display** - แสดงค่า Pips ใต้ราคา SL/TP ด้วยสีเหลืองเหมือน Lot Size
- **Improved Card Layout** - การจัดวางข้อมูลชัดเจนขึ้น
- **Enhanced Visual Hierarchy** - ข้อมูลสำคัญเด่นชัดกว่าเดิม
- **Mobile Card Optimization** - การ์ดขนาดเหมาะสมสำหรับ iPhone 14 Pro Max

### 🚀 ฟีเจอร์ใหม่ V4.2 (Enhanced UX & Responsive)
- **ปุ่มเพิ่มการ์ด** - เพิ่มการ์ดจากการคำนวณปัจจุบันเป็นการ์ดถาวร
- **ระบบบันทึกการ์ด** - บันทึกการคำนวณที่ต้องการไว้ใช้ในอนาคต
- **การแสดงผลแบบแยกบรรทัด** - กำไร/ขาดทุนแสดงแยกบรรทัดพร้อมสีที่ชัดเจน
- **Responsive Cards Grid** - การ์ดแสดงผลเหมาะสมทุกขนาดหน้าจอ
- **Mobile Optimized** - การ์ดแสดง 2 ใบต่อแถวบนมือถือ

### 🎨 การออกแบบ Responsive
- **📱 Mobile (iPhone 14 Pro Max)**: 2 การ์ดต่อแถว, UI ขนาดกะทัดรัด
- **📲 Tablet**: 2-3 การ์ดต่อแถว, เลย์เอาต์ 2 คอลัมน์
- **💻 Desktop**: 3-4 การ์ดต่อแถว, เลย์เอาต์ Calculator + Results
- **🖥️ Large Desktop**: 4+ การ์ดต่อแถว, เลย์เอาต์กว้างขวาง

### ✨ ฟีเจอร์หลัก V4.1 (RR Management)
- **เรียงลำดับการ์ดตาม RR** - การ์ดจัดเรียงตามลำดับ RR checkbox
- **TP Auto-RR Creation** - กรอก TP แล้วสร้าง RR อัตโนมัติเป็นลำดับแรก
- **Reset RR เป็น Default** - กด "คำนวณ" จะ reset RR เป็น 1:1, 1:2, 1:3, 1:10
- **Color Coding** - เขียวสำหรับกำไร, แดงสำหรับขาดทุน, เหลืองสำหรับเน้น

### 🔥 ฟีเจอร์หลัก V4.0 (Binance Style)
- **Binance Dark Theme** - ธีมสีดำสไตล์ Binance พร้อมสีมาตรฐาน
- **คำนวณอัตโนมัติ** - ไม่ต้องกดปุ่ม เมื่อกรอกข้อมูลครบจะคำนวณทันที
- **การจัดการ RR แบบ Checkbox** - เลือก RR ที่ต้องการได้หลายตัวพร้อมกัน
- **ลบ RR และ Card** - ลบ RR ที่ไม่ต้องการ การ์ดจะหายไปด้วย
- **SL ยืดหยุ่น** - รองรับการใส่ Stop Loss แบบ Pips หรือ ราคาโดยตรง
- **Local Storage** - บันทึกข้อมูลอัตโนมัติ ไม่ต้องกรอกใหม่

## 📱 การออกแบบ Binance Style

### เพิ่มประสิทธิภาพสำหรับ iPhone 14 Pro Max
- **ขนาดหน้าจอ**: 390x844px viewport
- **Theme**: Binance Dark Theme (#0B0E11, #1E2329, #F0B90B)
- **ฟอนต์**: Inter (Binance Standard Font)
- **สี**: Binance Color Palette (เหลือง=เน้น, เขียว=กำไร, แดง=ขาดทุน)
- **การใช้งาน**: Touch-optimized interface สไตล์ Binance

## 🛠️ วิธีการใช้งาน

### 1. ข้อมูลพื้นฐาน
```
1. ทุน (Capital) - ใส่จำนวนเงินทุนใน USD
2. ราคาเข้า (Entry Price) - ใส่ราคาทองที่ต้องการเข้า
3. ทิศทางการเทรด - เลือก BUY หรือ SELL
```

### 2. การตั้ง Stop Loss
```
- เลือกประเภท: Pips หรือ ราคา
- Pips: ใส่จำนวน Pips (เช่น 200)
- ราคา: ใส่ราคา SL โดยตรง (เช่น 2560.00)
```

### 3. Quick RR Selection
```
- เลือก RR ที่ต้องการจากปุ่ม (1:1, 1:2, 1:3, 1:5)
- เพิ่ม RR ใหม่: ใส่ตัวเลขแล้วกด "เพิ่ม RR"
- ลบ RR: hover บนปุ่ม RR แล้วกด X
- เรียง RR: ลากปุ่ม RR เพื่อเปลี่ยนลำดับ
```

### 4. ผลลัพธ์
```
แสดงเป็น Card แต่ละ RR ประกอบด้วย:
- Signal Type (BUY/SELL)
- RR Ratio (แสดงชัดเจน)
- Lot Size (ไฮไลท์)
- Entry Price (ไฮไลท์)
- Stop Loss (ไฮไลท์)
- Take Profit (ไฮไลท์)
- Profit/Loss คาดหวัง
```

## � Quick Deployment Guide

### 🌐 Live Demo
- **Production**: https://zicula.github.io/gold-trading-calculator/all_in_calculator_v4.html
- **V4 Calculator**: https://zicula.github.io/gold-trading-calculator/all_in_calculator_v4.html
- **Direct V4 Link**: https://zicula.github.io/gold-trading-calculator/all_in_calculator_v4.html
- **Repository**: https://github.com/zicula/gold-trading-calculator
- **Author**: Zic Trading

### ⚡ One-Click Deployment
```bash
# Run the automated deployment script
./deploy.sh
```

### 🔧 Manual Deployment Steps
```bash
# 1. Initialize Git & Push to GitHub
git init
git add .
git commit -m "🚀 Gold Trading Calculator V4 by Zic"
git remote add origin https://github.com/zicula/gold-trading-calculator.git
git push -u origin main

# 2. Deploy to Vercel (Free & Fast)
npm install -g vercel
vercel login
vercel --prod

# 3. Deploy to Netlify (Alternative)
npm install -g netlify-cli
netlify login
netlify deploy --prod --dir=.
```

### 📱 Access URLs
- **Main App**: `/all_in_calculator_v4.html` 
- **Landing Page**: `/index.html`
- **Direct Calculator**: `/calculator` (redirect)

## �🔧 การติดตั้งและใช้งาน

### วิธีที่ 1: ใช้งานท้องถิ่น (Local)
```bash
# วิธีที่ 1: Python HTTP Server
cd /path/to/Gold_Trading_Calculator
python3 -m http.server 8080

# วิธีที่ 2: Node.js
npx serve . -p 8080

# แล้วเปิด: http://localhost:8080/all_in_calculator_v3.html
```

### วิธีที่ 2: เปิดไฟล์โดยตรง
```
1. ดับเบิลคลิกที่ไฟล์ all_in_calculator_v3.html
2. จะเปิดในเบราว์เซอร์โดยตรง
3. ใช้งานได้ทันที (บางฟีเจอร์อาจจำกัด)
```

## 📊 สูตรการคำนวณ

### All In Calculation
```javascript
// ระยะห่าง SL ในหน่วย USD
stopDistanceUSD = Math.abs(entryPrice - stopLossPrice)

// Lot Size (ใช้เงินทุนทั้งหมด)
lotSize = capital / (contractSize * stopDistanceUSD)

// where: contractSize = 100 oz, pipValue = 0.01
```

### การแปลง Pips เป็นราคา
```javascript
// BUY: SL ต่ำกว่า Entry
stopLossPrice = entryPrice - (stopLossPips / 100)

// SELL: SL สูงกว่า Entry  
stopLossPrice = entryPrice + (stopLossPips / 100)
```

### การคำนวณ Take Profit
```javascript
// TP Pips = SL Pips × RR Ratio
takeProfitPips = stopLossPips * rrRatio

// BUY: TP สูงกว่า Entry
takeProfitPrice = entryPrice + (takeProfitPips / 100)

// SELL: TP ต่ำกว่า Entry
takeProfitPrice = entryPrice - (takeProfitPips / 100)
```

## 📈 ข้อมูลการเทรดทอง

| พารามิเตอร์ | ค่า |
|------------|-----|
| Contract Size | 100 oz/lot |
| Pip Value | $0.01 |
| Minimum Trade | 0.01 lot |
| Typical Spread | 3-5 pips |
| Trading Hours | 24/5 |

## 💡 ตัวอย่างการใช้งาน

### ตัวอย่าง 1: BUY Gold
```
ทุน: $1,000
Entry: $2,560.50
SL: 200 pips (2,558.50)
RR: 1:2

ผลลัพธ์:
- Lot Size: 0.50
- TP: $2,564.50 (400 pips)
- กำไรคาดหวัง: $2,000
```

### ตัวอย่าง 2: SELL Gold
```
ทุน: $500
Entry: $2,580.00
SL: $2,585.00 (500 pips)
RR: 1:3

ผลลัพธ์:
- Lot Size: 0.20
- TP: $2,565.00 (1,500 pips)
- กำไรคาดหวัง: $1,500
```

## ⚠️ คำเตือนและข้อควรระวัง

### 🚨 คำเตือนสำคัญ
- **การเทรด All In มีความเสี่ยงสูงมาก**
- อาจสูญเสียเงินทุนทั้งหมดได้
- ควรทดสอบด้วย Demo Account ก่อน
- เข้าใจกลยุทธ์และบริหารความเสี่ยงให้ดี

### 📱 การใช้งานบนมือถือ
- รองรับการสัมผัสและการลาก
- ออกแบบเฉพาะสำหรับ iPhone 14 Pro Max
- ใช้งานได้บนอุปกรณ์อื่นๆ ด้วย

### 🔧 การแก้ไขปัญหา
- ใช้เบราว์เซอร์ที่ทันสมัย (Chrome, Safari, Firefox)
- เปิดใช้งาน JavaScript
- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต (สำหรับฟอนต์และไอคอน)

## 📂 ไฟล์ในโปรเจค

```
Gold_Trading_Calculator/
├── all_in_calculator_v3.html     # ไฟล์หลัก (เวอร์ชั่นล่าสุด)
├── all_in_calculator_v2.html     # เวอร์ชั่นก่อนหน้า
├── all_in_calculator.html        # เวอร์ชั่นแรก
├── README.md                     # ไฟล์นี้
├── PROMPT_HISTORY.md            # ประวัติการพัฒนา
└── CHANGELOG.md                 # บันทึกการเปลี่ยนแปลง
```

## 🔄 การอัปเดต

### เวอร์ชั่นปัจจุบัน: V3.0
- ระบบคำนวณอัตโนมัติ
- การจัดการ RR และ Card ที่ดีขึ้น
- UI/UX ที่เหมาะกับมือถือมากขึ้น

### เวอร์ชั่นถัดไป: V4.0 (แผน)
- การเชื่อมต่อ API ราคาทองเรียลไทม์
- การบันทึกประวัติการคำนวณ
- การส่งออกข้อมูลเป็น PDF
- Multi-language support

## 📞 การติดต่อและสนับสนุน

- **เป้าหมาย**: สำหรับนักเทรดมืออาชีพ
- **กลยุทธ์**: "เทรดสั้น All In 1,000 เด้ง"
- **พัฒนาโดย**: GitHub Copilot AI Assistant
- **วันที่พัฒนา**: กรกฎาคม 2025

---

**⚡ All In Gold Trading Calculator V3**  
*Money Management Tool for Professional Gold Traders*

**🚀 "เทรดให้รวย คิดให้รอบคอบ วางแผนให้ดี"**
