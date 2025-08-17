# Frontend - Gold Trading Calculator

## 📁 โครงสร้าง

```
frontend/
├── assets/                 # Static assets (CSS, images, fonts)
│   └── styles.css         # Main stylesheet
├── components/            # HTML components
│   ├── all_in_calculator* # Calculator variants
│   ├── risk_calculator*   # Risk calculators
│   ├── lot-calculator.html # Lot size calculator
│   ├── mt5_integration.html # MT5 integration
│   ├── server.html        # Server interface
│   └── test.html          # Test components
├── js/                    # JavaScript files
│   ├── script.js          # Main application logic
│   ├── lot-calculator.js  # Lot calculator logic
│   └── server.js          # Server communication
├── index.html             # Main entry point
└── multi_account_calculator.html # Multi-account interface
```

## 🚀 การใช้งาน

### Development
```bash
# เปิดไฟล์ HTML ในเบราว์เซอร์
open frontend/index.html

# หรือใช้ local server
cd frontend
python -m http.server 8000
```

### Production
```bash
# Deploy ไป GitHub Pages
git add frontend/
git commit -m "Update frontend"
git push origin main
```

## 🔧 การแก้ไข

### แก้ไข CSS
- แก้ไขในไฟล์ `assets/styles.css`
- ใช้ CSS variables สำหรับ theming

### แก้ไข JavaScript
- แยก logic ตาม function ในโฟลเดอร์ `js/`
- ใช้ modules pattern เพื่อจัดการ code

### เพิ่ม Components
- สร้างไฟล์ HTML ใหม่ในโฟลเดอร์ `components/`
- Import ใน index.html หรือ multi_account_calculator.html

## 📱 Responsive Design

- รองรับ mobile, tablet, desktop
- ใช้ CSS Grid และ Flexbox
- Breakpoints: 768px, 1024px, 1200px

## 🎨 UI Guidelines

### Colors
- Primary: #007cba
- Success: #28a745
- Warning: #ffc107
- Error: #dc3545

### Typography
- Font: San Francisco, Helvetica, Arial
- Sizes: 12px, 14px, 16px, 18px, 24px, 32px

### Components
- Buttons: rounded corners, shadow effects
- Forms: clear labels, validation feedback
- Cards: subtle shadows, proper spacing
