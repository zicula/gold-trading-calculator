# 🤖 INSTRUCTION PROMPTS - Gold Trading Calculator Project

คำสั่งและ Prompts สำหรับการพัฒนาโปรเจ็คเครื่องคำนวณการเทรดทอง แบบ Kiro IDE Style (AWS AI-Powered Development)

---

## 🎯 PROJECT OVERVIEW

### 📋 Project Identity
- **Project Name**: Gold Trading Calculator V4 - Binance Style
- **Author**: Zic Trading
- **Technology Stack**: HTML5, CSS3, JavaScript (Vanilla), LocalStorage
- **Architecture**: Single Page Application (SPA)
- **Design System**: Binance Dark Theme
- **Current Version**: V4.7.0

### 🌐 Live Deployment
- **Production URL**: https://zicula.github.io/gold-trading-calculator/all_in_calculator_v4.html
- **Repository**: https://github.com/zicula/gold-trading-calculator
- **Deployment**: GitHub Pages (Auto-deploy from main branch)

---

## 🔧 KIRO IDE STYLE DEVELOPMENT WORKFLOW

### 📝 **Phase 1: Requirements Documentation** 
```
🎯 ก่อนเขียนโค้ด ต้องสร้างเอกสาร Requirement ให้ละเอียดก่อนเสมอ:

1. 📋 Feature Specification
   - ชื่อฟีเจอร์และวัตถุประสงค์
   - User Story และ Acceptance Criteria
   - UI/UX Requirements
   - Performance Requirements
   - Compatibility Requirements

2. 🎨 Design Documentation
   - UI Mockup/Wireframe (อธิบายด้วยคำ)
   - Binance Theme Integration Plan
   - Responsive Design Strategy
   - Multi-Language Support Plan

3. � Technical Specification
   - Implementation Approach
   - Code Structure Plan
   - Data Flow Design
   - LocalStorage Schema
   - Error Handling Strategy
```

### 📝 **Phase 2: Task Breakdown**
```
🧩 แตกเอกสาร Requirements เป็น Tasks ย่อยที่ทำได้ทีละขั้น:

1. 🏗️ HTML Structure Task
   - Create semantic HTML elements
   - Add data-key attributes for translations
   - Implement responsive grid structure
   - Add accessibility attributes

2. 🎨 CSS Styling Task
   - Implement Binance theme variables
   - Create responsive breakpoints
   - Add hover and transition effects
   - Ensure mobile-first design

3. ⚡ JavaScript Logic Task
   - Initialize DOM elements
   - Implement core functionality
   - Add event listeners
   - Handle user interactions

4. 💾 Data Persistence Task
   - Design localStorage schema
   - Implement save/load functions
   - Add error handling
   - Clean up old data

5. 🌐 Multi-Language Task
   - Add translation keys
   - Update translation dictionaries
   - Test language switching
   - Verify UI layout consistency

6. 📋 Documentation Task
   - Update CHANGELOG.md
   - Update README.md
   - Update PROMPT_HISTORY.md
   - Test live deployment
```

### 📝 **Phase 3: Implementation with Hooks**
```
🔗 ระบบ Hooks เพื่อตรวจสอบเงื่อนไขก่อนดำเนินการ:

1. 🔍 Pre-Code Hook
   ✅ Requirements document completed?
   ✅ Design approved?
   ✅ Task breakdown ready?
   ✅ Existing code analyzed?

2. 🎨 Pre-CSS Hook
   ✅ HTML structure completed?
   ✅ Binance theme variables defined?
   ✅ Responsive breakpoints planned?
   ✅ Mobile-first approach?

3. ⚡ Pre-JavaScript Hook
   ✅ CSS styling completed?
   ✅ DOM elements identified?
   ✅ Event flow designed?
   ✅ Error handling planned?

4. 🌐 Pre-Translation Hook
   ✅ All text elements have data-key?
   ✅ Translation keys follow naming convention?
   ✅ Both Thai and English translations ready?
   ✅ UI layout tested in both languages?

5. 📋 Pre-Documentation Hook
   ✅ All features implemented and tested?
   ✅ Version number updated?
   ✅ Live deployment verified?
   ✅ All documentation files current?

6. 🚀 Pre-Deployment Hook
   ✅ No console errors?
   ✅ Responsive design tested?
   ✅ Multi-language working?
   ✅ LocalStorage functioning?
   ✅ Git commit message semantic?
```

### 📝 **Phase 4: Continuous Validation**
```
🔄 ตรวจสอบเงื่อนไขอัตโนมัติตลอดกระบวนการ:

Rules ที่ต้องเป็นจริงเสมอ:
- 📱 แก้ไข HTML → ต้องตรวจสอบ Responsive Design
- 🎨 แก้ไข CSS → ต้องใช้ Binance Color Variables
- ⚡ แก้ไข JavaScript → ต้องเพิ่ม Error Handling
- 🌐 เพิ่ม Text → ต้องเพิ่ม Translation Keys
- 💾 เพิ่ม Data → ต้องเพิ่ม LocalStorage Schema
- 📋 เพิ่ม Feature → ต้อง Update Documentation
- 🚀 Push Code → ต้อง Test Live Deployment
```

---

## 🛠️ KIRO STYLE DEVELOPMENT COMMANDS

### 📋 **Requirements Generation Commands**
```bash
# Analyze existing feature patterns
grep -n "class\|function\|const" all_in_calculator_v4.html | head -20

# Check current translation coverage
grep -c "data-key" all_in_calculator_v4.html

# Analyze existing localStorage usage
grep -n "localStorage" all_in_calculator_v4.html

# Check Binance theme consistency
grep -n "--binance" all_in_calculator_v4.html
```

### 🧩 **Task Validation Commands**
```bash
# Validate HTML structure
grep -n "<div\|<button\|<input" all_in_calculator_v4.html | tail -10

# Check CSS responsive breakpoints
grep -n "@media" all_in_calculator_v4.html

# Validate JavaScript event listeners
grep -n "addEventListener" all_in_calculator_v4.html

# Check translation completeness
grep -n "data-key" all_in_calculator_v4.html | wc -l
```

### 🔗 **Hook Verification Commands**
```bash
# Pre-deployment validation
git status
npm run test 2>/dev/null || echo "No tests configured"
grep -n "console.error\|console.log" all_in_calculator_v4.html

# Live deployment check
curl -I https://zicula.github.io/gold-trading-calculator/all_in_calculator_v4.html
```

---

## 📋 KIRO STYLE DOCUMENTATION TEMPLATES

### 📝 **Requirements Document Template**
```markdown
# Feature Requirement: [Feature Name]

## 🎯 Feature Overview
- **Feature Name**: [ชื่อฟีเจอร์]
- **Purpose**: [วัตถุประสงค์]
- **Priority**: [High/Medium/Low]
- **Estimated Effort**: [Small/Medium/Large]

## 👤 User Stories
```
As a [user type]
I want [functionality]
So that [benefit]
```

## ✅ Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## 🎨 UI/UX Requirements
- **Visual Design**: [Binance theme compliance]
- **Responsive**: [Mobile/Tablet/Desktop behavior]
- **Accessibility**: [Screen reader support]
- **Performance**: [Loading time requirements]

## 🔧 Technical Requirements
- **Browser Support**: [Chrome, Firefox, Safari, Edge]
- **Device Support**: [Mobile, Tablet, Desktop]
- **Language Support**: [Thai, English]
- **Data Persistence**: [LocalStorage requirements]

## 🔗 Dependencies
- **Existing Features**: [Features this depends on]
- **External Libraries**: [None - Vanilla JS only]
- **API Integration**: [None - Client-side only]

## 🧪 Testing Plan
- [ ] Unit testing approach
- [ ] Integration testing plan
- [ ] User acceptance testing
- [ ] Multi-language testing
- [ ] Responsive design testing
```

### 🧩 **Task Breakdown Template**
```markdown
# Task Breakdown: [Feature Name]

## 📋 Task List
### Task 1: HTML Structure
- **Description**: Create semantic HTML elements
- **Deliverable**: HTML markup with data-key attributes
- **Dependencies**: Requirements document
- **Estimated Time**: [X hours]

### Task 2: CSS Styling
- **Description**: Implement Binance theme styling
- **Deliverable**: Responsive CSS with theme variables
- **Dependencies**: Task 1 completed
- **Estimated Time**: [X hours]

### Task 3: JavaScript Logic
- **Description**: Implement core functionality
- **Deliverable**: Working JavaScript with error handling
- **Dependencies**: Task 1, 2 completed
- **Estimated Time**: [X hours]

### Task 4: Translation Support
- **Description**: Add multi-language support
- **Deliverable**: Complete Thai/English translations
- **Dependencies**: All previous tasks
- **Estimated Time**: [X hours]

### Task 5: Documentation
- **Description**: Update project documentation
- **Deliverable**: Updated CHANGELOG, README, PROMPT_HISTORY
- **Dependencies**: Feature complete
- **Estimated Time**: [X hours]

## 🔗 Hook Checkpoints
- [ ] Pre-Code: Requirements approved
- [ ] Pre-CSS: HTML structure validated
- [ ] Pre-JS: CSS styling completed
- [ ] Pre-Translation: Core functionality working
- [ ] Pre-Documentation: All features tested
- [ ] Pre-Deployment: Documentation updated
```

---

## 🎯 KIRO STYLE QUALITY GATES

### ✅ **Quality Gate 1: Requirements Validation**
```
Mandatory checks before starting implementation:
□ User story clearly defined
□ Acceptance criteria measurable
□ UI/UX mockup described
□ Technical approach planned
□ Dependencies identified
□ Testing strategy defined
```

### ✅ **Quality Gate 2: Implementation Validation**
```
Mandatory checks during implementation:
□ Code follows existing patterns
□ Binance theme variables used
□ Error handling implemented
□ Translation keys added
□ Responsive design maintained
□ LocalStorage schema updated
```

### ✅ **Quality Gate 3: Deployment Validation**
```
Mandatory checks before deployment:
□ No console errors
□ Multi-language working
□ Responsive design tested
□ LocalStorage functioning
□ Live URL accessible
□ Documentation updated
□ Git commit semantic
□ Version number bumped
```

---

## 🔄 KIRO STYLE INTERACTION COUNTING

### � **Counted Interactions (คิดโควต้า)**
```
1. 🎯 Feature Request Analysis
2. 📋 Requirements Document Creation
3. 🧩 Task Breakdown Planning
4. 🔧 Implementation Guidance
5. 🐛 Bug Fix Analysis
6. 📊 Code Review Request
7. 🚀 Deployment Assistance
8. 📋 Documentation Updates
```

### 🤖 **Non-Counted Actions (ไม่คิดโควต้า)**
```
1. ⚡ Automatic Code Formatting
2. 🔍 Syntax Error Detection
3. 📝 Auto-generated Comments
4. 🔄 Automatic Imports
5. 🧹 Code Cleanup
6. 📊 Performance Monitoring
7. 🔗 Hook Validations
8. 📈 Statistics Updates
```

---

**📝 Last Updated**: July 21, 2025 
**🎯 Development Philosophy**: Kiro IDE Style - Documentation First, Step-by-Step Implementation
**🌐 Live Version**: V4.7.0 with Language Switcher
3. 🎯 Add CSS styling following Binance theme
4. ⚡ Implement JavaScript functionality
5. 💾 Add localStorage persistence if needed
6. 📱 Test responsive behavior
7. 🌐 Add multi-language support
8. 📋 Update documentation
```

### 📝 **Rule 5: Multi-Language Support**
```
Every text element must be translatable:
- Use data-key attributes for all text content
- Add translations to both 'th' and 'en' dictionaries
- Follow existing translation key naming convention
- Test language switching functionality
- Ensure UI layout works in both languages
```

### 📝 **Rule 6: LocalStorage Data Management**
```
Data persistence strategy:
- Use descriptive key names (goldCalculator prefix)
- Implement try-catch for localStorage operations
- Provide fallback values for missing data
- Clean up old/unused storage keys
- Respect user privacy (no external tracking)
```

### 📝 **Rule 7: Error Handling & Validation**
```
Robust error handling:
- Validate all user inputs before processing
- Provide clear error messages in both languages
- Use visual feedback for invalid states
- Implement graceful degradation
- Log errors for debugging (console only)
```

### 📝 **Rule 8: Performance Optimization**
```
Keep application performant:
- Minimize DOM queries (cache element references)
- Use event delegation for dynamic content
- Debounce rapid user interactions
- Optimize for mobile devices
- Keep bundle size minimal (no unnecessary libraries)
```

### 📝 **Rule 9: Version Control & Documentation**
```
Maintain clean development history:
- Use semantic commit messages
- Update CHANGELOG.md for each version
- Document breaking changes
- Keep README.md current with live URLs
- Update PROMPT_HISTORY.md for each session
```

---

## 🛠️ DEVELOPMENT COMMANDS

### 🔄 **Code Analysis Commands**
```bash
# Analyze current code structure
grep -n "class\|function\|const\|let" all_in_calculator_v4.html

# Find translation keys
grep -n "data-key" all_in_calculator_v4.html

# Check localStorage usage
grep -n "localStorage" all_in_calculator_v4.html

# Analyze CSS variables
grep -n "--binance" all_in_calculator_v4.html
```

### 🎨 **UI Development Commands**
```bash
# Check responsive breakpoints
grep -n "@media" all_in_calculator_v4.html

# Find color usage
grep -n "color:" all_in_calculator_v4.html

# Check font usage
grep -n "font-" all_in_calculator_v4.html
```

### 🚀 **Deployment Commands**
```bash
# Quick deploy workflow
git add .
git commit -m "feat: [feature description]"
git push origin main

# Check deployment status
git log --oneline -5

# Verify live site
curl -I https://zicula.github.io/gold-trading-calculator/all_in_calculator_v4.html
```

---

## 📋 FEATURE DEVELOPMENT TEMPLATES

### 🎯 **New Feature Template**
```javascript
// 1. Add to constructor
this.initializeNewFeature();

// 2. Create initialization method
initializeNewFeature() {
    // Setup feature-specific elements
    this.newFeatureElements = {
        button: document.getElementById('newFeatureBtn'),
        container: document.getElementById('newFeatureContainer')
    };
    
    // Attach event listeners
    this.newFeatureElements.button.addEventListener('click', () => {
        this.handleNewFeature();
    });
}

// 3. Implement feature logic
handleNewFeature() {
    try {
        // Feature implementation
        this.updateUI();
        this.saveFeatureToStorage();
    } catch (error) {
        console.error('New Feature Error:', error);
        this.showErrorMessage('feature-error');
    }
}

// 4. Add translations
// In translations.th:
'new-feature-label': 'ป้ายชื่อฟีเจอร์ใหม่',
'new-feature-button': 'ปุ่มฟีเจอร์ใหม่'

// In translations.en:
'new-feature-label': 'New Feature Label',
'new-feature-button': 'New Feature Button'
```

### 🎨 **CSS Component Template**
```css
/* New Feature Styling */
.new-feature-container {
    background: var(--binance-card);
    border: 1px solid var(--binance-border);
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}

.new-feature-button {
    background: var(--binance-yellow);
    color: var(--binance-dark);
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.new-feature-button:hover {
    background: var(--binance-yellow);
    opacity: 0.8;
}

/* Responsive */
@media (max-width: 767px) {
    .new-feature-container {
        padding: 12px;
        margin: 6px 0;
    }
}
```

### 📱 **HTML Structure Template**
```html
<!-- New Feature Section -->
<div class="new-feature-section">
    <div class="input-group">
        <div class="input-label">
            <i class="fas fa-icon" style="color: var(--binance-blue);"></i>
            <span data-key="new-feature-label">ป้ายชื่อฟีเจอร์</span>
        </div>
        <div class="new-feature-container">
            <button class="new-feature-button" id="newFeatureBtn">
                <i class="fas fa-plus"></i>
                <span data-key="new-feature-button">ปุ่มฟีเจอร์ใหม่</span>
            </button>
        </div>
    </div>
</div>
```

---

## 🎯 TESTING & QUALITY ASSURANCE

### ✅ **Pre-Deployment Checklist**
```
□ Feature works in both Thai and English
□ Responsive design tested on mobile/tablet/desktop
□ LocalStorage persistence verified
□ No console errors
□ Binance theme consistency maintained
□ Documentation updated
□ Git commit with proper message
□ Live URL tested after deployment
```

### 🔍 **Code Review Checklist**
```
□ Follows existing code patterns
□ Proper error handling implemented
□ Translation keys added for all text
□ CSS variables used for colors
□ Event listeners properly attached
□ Memory leaks prevented
□ Performance impact minimal
□ Cross-browser compatibility considered
```

---

## 📞 COMMUNICATION PROTOCOLS

### 💬 **User Request Handling**
```
When user requests a feature:
1. 🎯 Clarify requirements and scope
2. 🔍 Analyze existing codebase impact
3. 🎨 Propose UI/UX approach
4. ⚡ Implement with minimal changes
5. 🧪 Test thoroughly
6. 📋 Update documentation
7. 🚀 Deploy and verify
```

### 📊 **Progress Reporting**
```
For each development session:
1. ✅ Summary of completed features
2. 🔧 Technical implementation details
3. 🌐 Live deployment verification
4. 📋 Documentation updates
5. 🎯 Next steps or recommendations
```

---

## 🔮 FUTURE DEVELOPMENT GUIDELINES

### 🎯 **Feature Roadmap Considerations**
- Maintain Binance design system consistency
- Preserve mobile-first responsive approach
- Keep multi-language support complete
- Ensure backward compatibility
- Optimize for performance and user experience

### 🛡️ **Security & Privacy**
- No external data transmission
- LocalStorage only for user preferences
- No tracking or analytics (respect privacy)
- Secure coding practices
- Input validation and sanitization

---

**📝 Last Updated**: July 21, 2025
**🎯 Project Status**: Active Development
**🌐 Live Version**: V4.7.0 with Language Switcher
