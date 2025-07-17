// Gold Trading Lot Size Calculator
class GoldLotCalculator {
    constructor() {
        this.contractSize = 100; // 100 troy ounces per lot
        this.pipValue = 0.01; // 1 pip = $0.01 per 0.01 lot (200 pips = $2.00 for 1 lot)
        this.pipValuePerLot = 1; // $1 per 100 pips for 1 lot (200 pips = $2 for 1 lot)
        this.init();
    }

    init() {
        const form = document.getElementById('lotCalculatorForm');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.calculateLotSize();
        });

        // Auto-calculate on input change
        const inputs = ['totalCapital', 'riskPercent', 'entryPrice', 'stopLoss', 'takeProfit', 'tradeDirection'];
        inputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            if (input) {
                input.addEventListener('input', () => {
                    if (this.isFormValid()) {
                        this.calculateLotSize();
                    }
                });
            }
        });

        // Initialize with default calculation
        setTimeout(() => {
            if (this.isFormValid()) {
                this.calculateLotSize();
            }
        }, 100);
    }

    isFormValid() {
        const requiredFields = ['totalCapital', 'riskPercent', 'entryPrice', 'stopLoss'];
        return requiredFields.every(fieldId => {
            const field = document.getElementById(fieldId);
            return field && field.value && parseFloat(field.value) > 0;
        });
    }

    calculateLotSize() {
        if (!this.isFormValid()) {
            document.getElementById('resultsSection').style.display = 'none';
            return;
        }

        try {
            // Get input values
            const totalCapital = parseFloat(document.getElementById('totalCapital').value);
            const riskPercent = parseFloat(document.getElementById('riskPercent').value);
            const entryPrice = parseFloat(document.getElementById('entryPrice').value);
            const stopLoss = parseFloat(document.getElementById('stopLoss').value);
            const takeProfit = parseFloat(document.getElementById('takeProfit').value) || null;
            const direction = document.getElementById('tradeDirection').value;

            // Validate inputs
            if (!this.validateInputs(totalCapital, riskPercent, entryPrice, stopLoss, direction)) {
                return;
            }

            // Calculate risk amount
            const riskAmount = totalCapital * (riskPercent / 100);

            // Calculate stop loss distance
            let stopDistance;
            if (direction === 'long') {
                stopDistance = entryPrice - stopLoss;
                if (stopDistance <= 0) {
                    this.showError('สำหรับ Long: Stop Loss ต้องต่ำกว่าราคาเข้า');
                    return;
                }
            } else {
                stopDistance = stopLoss - entryPrice;
                if (stopDistance <= 0) {
                    this.showError('สำหรับ Short: Stop Loss ต้องสูงกว่าราคาเข้า');
                    return;
                }
            }

            // Calculate lot size
            // Risk Amount = Lot Size × Contract Size × Stop Distance
            // Lot Size = Risk Amount / (Contract Size × Stop Distance)
            const calculatedLot = riskAmount / (this.contractSize * stopDistance);

            // Round to appropriate decimal places
            const roundedLot = this.roundLotSize(calculatedLot);

            // Calculate actual values with rounded lot
            const actualRiskAmount = roundedLot * this.contractSize * stopDistance;
            const actualRiskPercent = (actualRiskAmount / totalCapital) * 100;
            const tradeValue = roundedLot * this.contractSize * entryPrice;

            // Calculate pip value for this lot size
            // For gold: 1 pip = $0.01 per 0.01 lot, so 200 pips = $2.00 for 1 lot
            const pipValueForLot = roundedLot * this.pipValuePerLot * 0.01; // $0.01 per pip per lot

            // Calculate take profit if provided
            let profitAmount = 0;
            let profitDistance = 0;
            let riskRewardRatio = 'ไม่ระบุ TP';

            if (takeProfit && takeProfit > 0) {
                if (direction === 'long') {
                    profitDistance = takeProfit - entryPrice;
                    if (profitDistance <= 0) {
                        this.showWarning('สำหรับ Long: Take Profit ควรสูงกว่าราคาเข้า');
                    }
                } else {
                    profitDistance = entryPrice - takeProfit;
                    if (profitDistance <= 0) {
                        this.showWarning('สำหรับ Short: Take Profit ควรต่ำกว่าราคาเข้า');
                    }
                }

                if (profitDistance > 0) {
                    profitAmount = roundedLot * this.contractSize * profitDistance;
                    const ratio = profitDistance / stopDistance;
                    riskRewardRatio = `1:${ratio.toFixed(2)}`;
                }
            }

            // Display results
            this.displayResults({
                lotSize: roundedLot,
                tradeValue: tradeValue,
                maxRisk: actualRiskAmount,
                actualRiskPercent: actualRiskPercent,
                expectedProfit: profitAmount,
                stopDistance: stopDistance,
                riskRewardRatio: riskRewardRatio,
                pipValue: pipValueForLot,
                direction: direction,
                entryPrice: entryPrice,
                stopLoss: stopLoss,
                takeProfit: takeProfit,
                riskPercent: riskPercent
            });

        } catch (error) {
            console.error('Calculation error:', error);
            this.showError('เกิดข้อผิดพลาดในการคำนวณ กรุณาตรวจสอบข้อมูล');
        }
    }

    validateInputs(totalCapital, riskPercent, entryPrice, stopLoss, direction) {
        if (totalCapital < 100) {
            this.showError('เงินทุนต้องมากกว่า $100');
            return false;
        }

        if (riskPercent < 0.1 || riskPercent > 10) {
            this.showError('ความเสี่ยงต้องอยู่ระหว่าง 0.1% - 10%');
            return false;
        }

        if (entryPrice < 1000 || entryPrice > 5000) {
            this.showError('ราคาทองต้องอยู่ระหว่าง $1,000 - $5,000');
            return false;
        }

        if (stopLoss < 1000 || stopLoss > 5000) {
            this.showError('Stop Loss ต้องอยู่ระหว่าง $1,000 - $5,000');
            return false;
        }

        return true;
    }

    roundLotSize(lotSize) {
        // Round to 4 decimal places for precision
        return Math.round(lotSize * 10000) / 10000;
    }

    displayResults(data) {
        // Show results section
        document.getElementById('resultsSection').style.display = 'block';

        // Update values
        document.getElementById('calculatedLot').textContent = data.lotSize.toFixed(4);
        document.getElementById('tradeValue').textContent = this.formatCurrency(data.tradeValue);
        document.getElementById('maxRisk').textContent = this.formatCurrency(data.maxRisk);
        document.getElementById('expectedProfit').textContent = data.expectedProfit > 0 ? 
            this.formatCurrency(data.expectedProfit) : 'ไม่ระบุ TP';
        document.getElementById('stopDistance').textContent = data.stopDistance.toFixed(2);
        document.getElementById('rrRatio').textContent = data.riskRewardRatio;
        document.getElementById('pipValue').textContent = this.formatCurrency(data.pipValue);
        document.getElementById('displayRisk').textContent = data.riskPercent + '%';

        // Generate summary
        this.generateSummary(data);

        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });

        // Hide any error messages
        this.hideErrors();
    }

    generateSummary(data) {
        const summary = document.getElementById('tradingSummary');
        const directionText = data.direction === 'long' ? 'ซื้อ (Long)' : 'ขาย (Short)';
        const profitText = data.takeProfit ? 
            `<br>• <strong>Take Profit:</strong> $${data.takeProfit.toFixed(2)}` : '';
        
        const riskPercentDisplay = data.actualRiskPercent.toFixed(2);
        const marginRequired = (data.tradeValue * 0.01); // Assuming 1% margin
        
        summary.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <strong>📊 รายละเอียดการเทรด:</strong><br>
                    • <strong>ทิศทาง:</strong> ${directionText}<br>
                    • <strong>ราคาเข้า:</strong> $${data.entryPrice.toFixed(2)}<br>
                    • <strong>Stop Loss:</strong> $${data.stopLoss.toFixed(2)}${profitText}<br>
                    • <strong>Lot Size:</strong> ${data.lotSize.toFixed(4)} lots
                </div>
                <div class="col-md-6">
                    <strong>💰 การจัดการเงิน:</strong><br>
                    • <strong>มูลค่าการเทรด:</strong> ${this.formatCurrency(data.tradeValue)}<br>
                    • <strong>ความเสี่ยงจริง:</strong> ${this.formatCurrency(data.maxRisk)} (${riskPercentDisplay}%)<br>
                    • <strong>Margin ประมาณ:</strong> ${this.formatCurrency(marginRequired)}<br>
                    • <strong>Value per Pip:</strong> ${this.formatCurrency(data.pipValue)}
                </div>
            </div>
        `;
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount);
    }

    showError(message) {
        this.hideErrors();
        
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            <i class="fas fa-exclamation-circle"></i>
            <strong>ข้อผิดพลาด:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        const form = document.getElementById('lotCalculatorForm');
        form.parentNode.insertBefore(alertDiv, form.nextSibling);

        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);

        // Hide results
        document.getElementById('resultsSection').style.display = 'none';
    }

    showWarning(message) {
        // Remove existing warnings
        const existingWarning = document.querySelector('.alert-warning.auto-warning');
        if (existingWarning) {
            existingWarning.remove();
        }
        
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-warning alert-dismissible fade show auto-warning';
        alertDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            <strong>คำเตือน:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        const form = document.getElementById('lotCalculatorForm');
        form.parentNode.insertBefore(alertDiv, form.nextSibling);

        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    hideErrors() {
        const alerts = document.querySelectorAll('.alert-danger, .alert-warning.auto-warning');
        alerts.forEach(alert => alert.remove());
    }
}

// Reset form function
function resetForm() {
    document.getElementById('lotCalculatorForm').reset();
    document.getElementById('resultsSection').style.display = 'none';
    
    // Remove alerts
    const alerts = document.querySelectorAll('.alert-danger, .alert-warning.auto-warning');
    alerts.forEach(alert => alert.remove());
    
    // Reset to default values
    document.getElementById('totalCapital').value = 10000;
    document.getElementById('riskPercent').value = 2;
    document.getElementById('entryPrice').value = 2000.00;
    document.getElementById('stopLoss').value = 1990.00;
    document.getElementById('takeProfit').value = 2020.00;
    document.getElementById('tradeDirection').value = 'long';
}

// Quick preset functions
function setQuickPreset(preset) {
    switch(preset) {
        case 'conservative':
            document.getElementById('riskPercent').value = 1;
            break;
        case 'moderate':
            document.getElementById('riskPercent').value = 2;
            break;
        case 'aggressive':
            document.getElementById('riskPercent').value = 3;
            break;
    }
    if (calculator && calculator.isFormValid()) {
        calculator.calculateLotSize();
    }
}

// Calculate lot size for specific dollar risk
function calculateForDollarRisk(dollarAmount) {
    const totalCapital = parseFloat(document.getElementById('totalCapital').value);
    if (totalCapital > 0) {
        const riskPercent = (dollarAmount / totalCapital) * 100;
        document.getElementById('riskPercent').value = riskPercent.toFixed(2);
        if (calculator && calculator.isFormValid()) {
            calculator.calculateLotSize();
        }
    }
}

// Initialize calculator
let calculator;
document.addEventListener('DOMContentLoaded', function() {
    calculator = new GoldLotCalculator();
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'Enter':
                    e.preventDefault();
                    if (calculator.isFormValid()) {
                        calculator.calculateLotSize();
                    }
                    break;
                case 'r':
                    e.preventDefault();
                    resetForm();
                    break;
            }
        }
    });
});

// Market hours and trading session info
const goldMarketInfo = {
    tradingHours: 'จันทร์ 6:00 น. - เสาร์ 5:00 น. (เวลาไทย)',
    bestTradingTimes: [
        'London Session: 14:00-23:00 น.',
        'New York Session: 20:00-05:00 น.',
        'Overlap: 20:00-23:00 น. (ปริมาณการซื้อขายสูงสุด)'
    ],
    volatilityFactors: [
        'ข่าวเศรษฐกิจสหรัฐฯ',
        'ค่าเงินดอลลาร์สหรัฐฯ',
        'ความไม่แน่นอนทางการเมือง',
        'อัตราดอกเบียงของธนาคารกลาง'
    ]
};
