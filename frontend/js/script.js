// Gold Trading Calculator - Money Management
class GoldTradingCalculator {
    constructor() {
        this.goldContractSize = 100; // 1 lot = 100 oz
        this.pipValue = 0.01; // 1 pip = $0.01 for gold
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateLabels();
    }

    bindEvents() {
        // Calculate button
        document.getElementById('calculateBtn').addEventListener('click', () => {
            this.calculate();
        });

        // Reset button
        document.getElementById('resetBtn').addEventListener('click', () => {
            this.reset();
        });

        // Radio button changes
        document.querySelectorAll('input[name="slType"]').forEach(radio => {
            radio.addEventListener('change', () => {
                this.updateLabels();
            });
        });

        document.querySelectorAll('input[name="tpType"]').forEach(radio => {
            radio.addEventListener('change', () => {
                this.updateLabels();
            });
        });

        // Real-time validation
        document.querySelectorAll('input[type="number"]').forEach(input => {
            input.addEventListener('input', () => {
                this.validateInput(input);
            });
        });
    }

    updateLabels() {
        const slType = document.querySelector('input[name="slType"]:checked').value;
        const tpType = document.querySelector('input[name="tpType"]:checked').value;

        const slLabel = document.getElementById('slLabel');
        const tpLabel = document.getElementById('tpLabel');
        const slInput = document.getElementById('stopLoss');
        const tpInput = document.getElementById('takeProfit');

        // Update Stop Loss label and placeholder
        switch(slType) {
            case 'price':
                slLabel.textContent = 'Stop Loss (ราคา)';
                slInput.placeholder = '2015.50';
                slInput.step = '0.01';
                break;
            case 'pips':
                slLabel.textContent = 'Stop Loss (Pips)';
                slInput.placeholder = '50';
                slInput.step = '1';
                break;
            case 'percent':
                slLabel.textContent = 'Stop Loss (% จากทุน)';
                slInput.placeholder = '2';
                slInput.step = '0.1';
                break;
        }

        // Update Take Profit label and placeholder
        switch(tpType) {
            case 'price':
                tpLabel.textContent = 'Take Profit (ราคา)';
                tpInput.placeholder = '2030.50';
                tpInput.step = '0.01';
                break;
            case 'pips':
                tpLabel.textContent = 'Take Profit (Pips)';
                tpInput.placeholder = '100';
                tpInput.step = '1';
                break;
            case 'ratio':
                tpLabel.textContent = 'Risk:Reward Ratio';
                tpInput.placeholder = '2';
                tpInput.step = '0.1';
                break;
        }
    }

    validateInput(input) {
        const value = parseFloat(input.value);
        if (isNaN(value) || value < 0) {
            input.style.borderColor = '#e74c3c';
            return false;
        } else {
            input.style.borderColor = '#27ae60';
            return true;
        }
    }

    calculate() {
        try {
            // Get input values
            const accountBalance = parseFloat(document.getElementById('accountBalance').value);
            const riskPercent = parseFloat(document.getElementById('riskPercent').value);
            const entryPrice = parseFloat(document.getElementById('entryPrice').value);
            const direction = document.getElementById('direction').value;
            const slType = document.querySelector('input[name="slType"]:checked').value;
            const tpType = document.querySelector('input[name="tpType"]:checked').value;
            const stopLossValue = parseFloat(document.getElementById('stopLoss').value);
            const takeProfitValue = parseFloat(document.getElementById('takeProfit').value);

            // Validate inputs
            if (!this.validateInputs(accountBalance, riskPercent, entryPrice, stopLossValue, takeProfitValue)) {
                return;
            }

            // Calculate risk amount
            const riskAmount = accountBalance * (riskPercent / 100);

            // Calculate Stop Loss price
            let stopLossPrice;
            switch(slType) {
                case 'price':
                    stopLossPrice = stopLossValue;
                    break;
                case 'pips':
                    if (direction === 'long') {
                        stopLossPrice = entryPrice - (stopLossValue * this.pipValue);
                    } else {
                        stopLossPrice = entryPrice + (stopLossValue * this.pipValue);
                    }
                    break;
                case 'percent':
                    const percentLoss = accountBalance * (stopLossValue / 100);
                    const pipsFromPercent = percentLoss / (this.goldContractSize * this.pipValue);
                    if (direction === 'long') {
                        stopLossPrice = entryPrice - (pipsFromPercent * this.pipValue);
                    } else {
                        stopLossPrice = entryPrice + (pipsFromPercent * this.pipValue);
                    }
                    break;
            }

            // Calculate Take Profit price
            let takeProfitPrice;
            const slDistance = Math.abs(entryPrice - stopLossPrice);
            
            switch(tpType) {
                case 'price':
                    takeProfitPrice = takeProfitValue;
                    break;
                case 'pips':
                    if (direction === 'long') {
                        takeProfitPrice = entryPrice + (takeProfitValue * this.pipValue);
                    } else {
                        takeProfitPrice = entryPrice - (takeProfitValue * this.pipValue);
                    }
                    break;
                case 'ratio':
                    if (direction === 'long') {
                        takeProfitPrice = entryPrice + (slDistance * takeProfitValue);
                    } else {
                        takeProfitPrice = entryPrice - (slDistance * takeProfitValue);
                    }
                    break;
            }

            // Calculate position size
            const slPips = Math.abs(entryPrice - stopLossPrice) / this.pipValue;
            const positionSize = riskAmount / (slPips * this.pipValue * this.goldContractSize);
            
            // Calculate trade value
            const tradeValue = positionSize * entryPrice * this.goldContractSize;

            // Calculate P&L
            const maxLoss = -riskAmount;
            const tpPips = Math.abs(entryPrice - takeProfitPrice) / this.pipValue;
            const expectedProfit = tpPips * this.pipValue * this.goldContractSize * positionSize;

            // Calculate Risk:Reward ratio
            const riskRewardRatio = expectedProfit / riskAmount;

            // Validate calculations
            if (!this.validateCalculations(stopLossPrice, takeProfitPrice, entryPrice, direction)) {
                return;
            }

            // Display results
            this.displayResults({
                riskAmount,
                positionSize,
                tradeValue,
                entryPrice,
                stopLossPrice,
                takeProfitPrice,
                slPips,
                tpPips,
                maxLoss,
                expectedProfit,
                riskRewardRatio,
                direction,
                riskPercent,
                slType,
                tpType
            });

            this.showAlert('คำนวณสำเร็จ!', 'success');

        } catch (error) {
            console.error('Calculation error:', error);
            this.showAlert('เกิดข้อผิดพลาดในการคำนวณ', 'error');
        }
    }

    validateInputs(accountBalance, riskPercent, entryPrice, stopLossValue, takeProfitValue) {
        if (isNaN(accountBalance) || accountBalance <= 0) {
            this.showAlert('กรุณาใส่ยอดเงินในบัญชีที่ถูกต้อง', 'error');
            return false;
        }

        if (isNaN(riskPercent) || riskPercent <= 0 || riskPercent > 10) {
            this.showAlert('กรุณาใส่เปอร์เซ็นต์ความเสี่ยงระหว่าง 0.1-10%', 'error');
            return false;
        }

        if (isNaN(entryPrice) || entryPrice <= 0) {
            this.showAlert('กรุณาใส่ราคาเข้าที่ถูกต้อง', 'error');
            return false;
        }

        if (isNaN(stopLossValue) || stopLossValue <= 0) {
            this.showAlert('กรุณาใส่ค่า Stop Loss ที่ถูกต้อง', 'error');
            return false;
        }

        if (isNaN(takeProfitValue) || takeProfitValue <= 0) {
            this.showAlert('กรุณาใส่ค่า Take Profit ที่ถูกต้อง', 'error');
            return false;
        }

        return true;
    }

    validateCalculations(stopLossPrice, takeProfitPrice, entryPrice, direction) {
        // Validate Stop Loss direction
        if (direction === 'long' && stopLossPrice >= entryPrice) {
            this.showAlert('Stop Loss ต้องต่ำกว่าราคาเข้าสำหรับ Long position', 'error');
            return false;
        }

        if (direction === 'short' && stopLossPrice <= entryPrice) {
            this.showAlert('Stop Loss ต้องสูงกว่าราคาเข้าสำหรับ Short position', 'error');
            return false;
        }

        // Validate Take Profit direction
        if (direction === 'long' && takeProfitPrice <= entryPrice) {
            this.showAlert('Take Profit ต้องสูงกว่าราคาเข้าสำหรับ Long position', 'error');
            return false;
        }

        if (direction === 'short' && takeProfitPrice >= entryPrice) {
            this.showAlert('Take Profit ต้องต่ำกว่าราคาเข้าสำหรับ Short position', 'error');
            return false;
        }

        return true;
    }

    displayResults(results) {
        // Show results container
        document.getElementById('resultsContainer').style.display = 'block';

        // Update Risk Management section
        document.getElementById('riskAmount').textContent = `$${results.riskAmount.toFixed(2)}`;
        document.getElementById('positionSize').textContent = results.positionSize.toFixed(3);
        document.getElementById('tradeValue').textContent = `$${results.tradeValue.toFixed(2)}`;

        // Update Trade Details section
        document.getElementById('finalEntryPrice').textContent = `$${results.entryPrice.toFixed(2)}`;
        document.getElementById('finalStopLoss').textContent = `$${results.stopLossPrice.toFixed(2)}`;
        document.getElementById('finalTakeProfit').textContent = `$${results.takeProfitPrice.toFixed(2)}`;
        document.getElementById('slPips').textContent = results.slPips.toFixed(1);
        document.getElementById('tpPips').textContent = results.tpPips.toFixed(1);
        document.getElementById('riskReward').textContent = `1:${results.riskRewardRatio.toFixed(2)}`;

        // Update P&L section
        document.getElementById('maxLoss').textContent = `$${results.maxLoss.toFixed(2)}`;
        document.getElementById('expectedProfit').textContent = `+$${results.expectedProfit.toFixed(2)}`;

        // Update Trading Summary
        const directionBadge = document.getElementById('tradingDirection');
        directionBadge.textContent = results.direction.toUpperCase();
        directionBadge.className = `direction-badge ${results.direction}`;

        document.getElementById('riskPercentDisplay').textContent = `${results.riskPercent.toFixed(2)}%`;
        document.getElementById('rrRatioDisplay').textContent = `1:${results.riskRewardRatio.toFixed(2)}`;
        
        // Convert types to Thai
        const slTypeMap = {
            'price': 'ราคา',
            'pips': 'Pips',
            'percent': 'เปอร์เซ็นต์'
        };
        const tpTypeMap = {
            'price': 'ราคา',
            'pips': 'Pips',
            'ratio': 'Risk:Reward Ratio'
        };

        document.getElementById('slTypeDisplay').textContent = slTypeMap[results.slType];
        document.getElementById('tpTypeDisplay').textContent = tpTypeMap[results.tpType];

        // Scroll to results
        document.getElementById('resultsContainer').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }

    reset() {
        // Clear all inputs
        document.getElementById('accountBalance').value = '10000';
        document.getElementById('riskPercent').value = '2';
        document.getElementById('entryPrice').value = '';
        document.getElementById('direction').value = 'long';
        document.getElementById('stopLoss').value = '';
        document.getElementById('takeProfit').value = '';

        // Reset radio buttons
        document.querySelector('input[name="slType"][value="price"]').checked = true;
        document.querySelector('input[name="tpType"][value="price"]').checked = true;

        // Hide results
        document.getElementById('resultsContainer').style.display = 'none';

        // Reset input borders
        document.querySelectorAll('input[type="number"]').forEach(input => {
            input.style.borderColor = '#e0e0e0';
        });

        // Update labels
        this.updateLabels();

        this.showAlert('รีเซ็ตข้อมูลแล้ว', 'success');
    }

    showAlert(message, type) {
        const alertContainer = document.getElementById('alertContainer');
        const alert = document.createElement('div');
        alert.className = `alert ${type}`;
        alert.innerHTML = `
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-exclamation-triangle'}"></i>
            ${message}
        `;

        alertContainer.appendChild(alert);

        // Remove alert after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        }, 5000);

        // Add click to dismiss
        alert.addEventListener('click', () => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        });
    }

    // Utility function to format currency
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount);
    }

    // Utility function to format percentage
    formatPercentage(value) {
        return `${value.toFixed(2)}%`;
    }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new GoldTradingCalculator();
});

// Add some additional utility functions
window.addEventListener('load', () => {
    // Add loading animation to calculate button
    const calculateBtn = document.getElementById('calculateBtn');
    calculateBtn.addEventListener('click', function() {
        this.classList.add('loading');
        setTimeout(() => {
            this.classList.remove('loading');
        }, 500);
    });

    // Add real-time currency formatting
    document.querySelectorAll('input[type="number"]').forEach(input => {
        if (input.id === 'accountBalance' || input.id === 'entryPrice') {
            input.addEventListener('blur', function() {
                const value = parseFloat(this.value);
                if (!isNaN(value)) {
                    this.value = value.toFixed(2);
                }
            });
        }
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            document.getElementById('calculateBtn').click();
        }
        if (e.ctrlKey && e.key === 'r') {
            e.preventDefault();
            document.getElementById('resetBtn').click();
        }
    });
});

// PWA support (if needed in the future)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Can add service worker registration here for offline support
    });
}
